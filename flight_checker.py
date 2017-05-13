'''
Created on 26 Sep 2016

@author: Alex Roan
'''
from skyscanner.skyscanner import Flights, FlightsCache, Hotels
from flight_classes import CacheAdventure, FlightItinerary
import operator
from datetime import datetime, timedelta

class FlightChecker:
    
    def __init__(self, browse_key, live_key, market, currency, locale):
        self.market = market
        self.currency = currency
        self.locale = locale
        self.flights_cache = FlightsCache(browse_key)
        self.live_key = live_key
           
    #Returns a list where the first item is the place Name, the second is the IATA code 
    def get_place_details(self, places, place_id):
        details = list()
        for place in places:
            if place['PlaceId'] == place_id:
                details.append(place['Name'])
                details.append(place['IataCode'])
                return details
    
    def get_place_name_from_flights(self, places, place_id):
        for place in places:
            if place['Id'] == place_id:
                return place['Name']
    
    #First in list is name, then second is image url
    def get_agent_details(self, agents, agent_id):
        details = list()
        for agent in agents:
            if agent['Id'] == agent_id:
                details.append(agent['Name'])
                details.append(agent['ImageUrl'])
                return details
     
    def get_leg_details(self, legs, leg_id):
        for leg in legs:
            if leg['Id'] == leg_id:
                return leg
            
    def get_carrier_names(self, carriers, journey):
        journey_carriers = list()
        for journey_carrier_id in journey['CarrierIds']:
            journey_carriers.append(self.get_carrier_name(carriers, journey_carrier_id))
        return journey_carriers
    
    def get_carrier_name(self, carriers, carrier_id):
        for carrier in carriers:
            if carrier['CarrierId'] == carrier_id:
                return carrier['Name']
    
    def next_weekday(self, d, weekday):
        days_ahead = weekday - d.weekday()
        if days_ahead <= 0: # Target day already happened this week
            days_ahead += 7
        return d + datetime.timedelta(days_ahead)
    
    def append_if_doesnt_exist(self, target, source, key_name, attribute_name):
        found_existing = False
        for source_item in source[key_name]:
            for target_item in target[key_name]:
                if source_item[attribute_name] == target_item[attribute_name]:
                    found_existing = True
                    break
            if found_existing == False:
                target[key_name].append(source_item)
                found_existing = False
        return target
    

    def browse_cache_by_route_advenchas(self, search_params):
        i = 0 
        cache_results = {}
        while i < len(search_params.departure_dates):
            departure_date = search_params.departure_dates[i]
            return_date = search_params.return_dates[i]
            try:    
                result = self.flights_cache.get_cheapest_price_by_route(
                                market=self.market,
                                currency=search_params.currency,
                                locale=self.locale,
                                originplace=search_params.origin,
                                destinationplace=search_params.destination,
                                outbounddate=departure_date.strftime('%Y-%m-%d'),
                                inbounddate=return_date.strftime('%Y-%m-%d')
                                ).parsed
            except Exception as exc:
                print('ERROR: Could not access browse cache by route')
                continue

            quotes = result['Quotes']
            carriers = result['Carriers']
            places = result['Places']
            for quote in quotes:
                min_price = quote['MinPrice']
                direct = quote['Direct']
                price = quote['MinPrice']
                cache_date = quote['QuoteDateTime']
                
                dept = quote['OutboundLeg']
                ret = quote['InboundLeg']
                
                dept_date = dept['DepartureDate']
                dept_place_details = self.get_place_details(places, dept['OriginId'])
                dept_place = dept_place_details[0]
                dept_iata = dept_place_details[1]
                dept_carriers = self.get_carrier_names(carriers, dept)

                ret_date = ret['DepartureDate']
                ret_place_details = self.get_place_details(places, ret['OriginId'])
                ret_place = ret_place_details[0]
                ret_iata = ret_place_details[1]
                ret_carriers = self.get_carrier_names(carriers, ret)
                
                datetime_now = datetime.now()
                cache_datetime = datetime.strptime(cache_date, "%Y-%m-%dT%H:%M:%S")
                #check that the return location is correct and flights are direct and the cache date is less than 24 hours ago
                if search_params.origin == dept_iata and direct == True and (datetime_now - cache_datetime) < timedelta(2):
                    advencha = CacheAdventure(
                                         price=price, 
                                         direct=direct, 
                                         dept_date=dept_date, 
                                         dept_place=dept_place, 
                                         dept_iata=dept_iata, 
                                         dept_carriers=dept_carriers, 
                                         ret_date=ret_date, 
                                         ret_place=ret_place, 
                                         ret_iata=ret_iata, 
                                         ret_carriers=ret_carriers, 
                                         cache_date=cache_date
                                         )
                    if ret_place in cache_results:
                        cache_results[ret_place].append(advencha)
                    else:
                        cache_results[ret_place] = [advencha]
            i += 1
        return cache_results

     
    def live_flights_query(self, adventure, adults, max_price_pp, earliest_dept_time, latest_dept_time, earliest_ret_time, latest_ret_time):     
        self.flights = Flights(self.live_key)
        try:
            result = self.flights.get_result(
                                country=self.market,
                                currency=self.currency,
                                locale=self.locale,
                                originplace=adventure.departure_iata+"-sky",
                                destinationplace=adventure.return_iata+"-sky",
                                outbounddate=adventure.departure_date.split('T')[0],
                                inbounddate=adventure.return_date.split('T')[0],
                                adults=adults,
                                groupPricing=True,
                                outbounddepartstarttime=earliest_dept_time,
                                outbounddepartendtime=latest_dept_time,
                                inbounddepartstarttime=earliest_ret_time,
                                inbounddepartendtime=latest_ret_time
                                ).parsed
            return result
        except Exception:
            print("ERROR: Exception trying to access Flights API:\n")
            print(str(Exception))

    def parse_live_price(self, result, adults, max_price_pp):
        itineraries = result['Itineraries']
        legs = result['Legs']
        places = result['Places']
        agents = result['Agents']
        cheap_itineraries = list()
        for itinerary in itineraries:
            pricing = itinerary['PricingOptions']
            for price in pricing:
                full_price = price['Price']
                if full_price <= max_price_pp:
                    flight_agents = list()
                    for single_agent in price['Agents']:
                        flight_agents.append(self.get_agent_details(agents, single_agent))
                    if 'DeeplinkUrl' in price:
                        link = price['DeeplinkUrl']
                        outbound_leg_details = self.get_leg_details(legs, itinerary['OutboundLegId'])
                        inbound_leg_details = self.get_leg_details(legs, itinerary['InboundLegId'])
                        dept_from = self.get_place_name_from_flights(places, outbound_leg_details['OriginStation'])
                        dept_time = outbound_leg_details['Departure']
                        dept_duration = outbound_leg_details['Duration']
                        dept_stops = len(outbound_leg_details['Stops'])
                        dept_arrive_location = self.get_place_name_from_flights(places, outbound_leg_details['DestinationStation'])
                        dept_arrive_time = outbound_leg_details['Arrival']
                        ret_from = self.get_place_name_from_flights(places, inbound_leg_details['OriginStation'])
                        ret_time = inbound_leg_details['Departure']
                        ret_duration = inbound_leg_details['Duration']
                        ret_stops = len(inbound_leg_details['Stops'])
                        ret_arrive_location = self.get_place_name_from_flights(places, inbound_leg_details['DestinationStation'])
                        ret_arrive_time = inbound_leg_details['Arrival']
                        flight_itinerary = FlightItinerary(
                            price=full_price,
                            agents=flight_agents,
                            link=link,
                            adults=adults,
                            dept_from=dept_from,
                            dept_time=dept_time,
                            dept_duration=dept_duration,
                            dept_stops=dept_stops,
                            dept_arrive_location=dept_arrive_location,
                            dept_arrive_time=dept_arrive_time,
                            ret_from=ret_from,
                            ret_time=ret_time,
                            ret_duration=ret_duration,
                            ret_stops=ret_stops,
                            ret_arrive_location=ret_arrive_location,
                            ret_arrive_time=ret_arrive_time
                            )
                        cheap_itineraries.append(flight_itinerary)
        return cheap_itineraries

