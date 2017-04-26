'''
Created on 26 Sep 2016

@author: Alex Roan
'''
from skyscanner.skyscanner import Flights, FlightsCache, Hotels
from flight_classes import CacheAdventure, FlightItinerary
import datetime, operator

class FlightChecker:
    
    def __init__(self, browse_key, live_key, market, currency, locale):
        self.market = market
        self.currency = currency
        self.locale = locale
        self.flights_cache = FlightsCache(browse_key)
        self.flights = Flights(live_key)
           
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
    

    def browse_cache_quotes(self, origin, destination, max_price_pp, weekly_departure_day, weekly_return_day, weeks_ahead):
        
        d = datetime.datetime.now()
        next_friday = self.next_weekday(d, weekly_departure_day)
        next_sunday = self.next_weekday(d, weekly_return_day)
        cache_results = list()
        count = 0
        while count < weeks_ahead:
            try:
                result = self.flights_cache.get_cheapest_quotes(
                                       market=self.market,
                                       currency=self.currency,
                                       locale=self.locale,
                                       originplace=origin,
                                       destinationplace=destination,
                                       outbounddate=next_friday.strftime('%Y-%m-%d'),
                                       inbounddate=next_sunday.strftime('%Y-%m-%d')
                                       ).parsed
            except Exception:
                print("ERROR: Exception trying to access Browse Cache API:\n")
                print(str(Exception))
                continue                
            quotes = result['Quotes']
            carriers = result['Carriers']
            places = result['Places']
            for quote in quotes:
                min_price = quote['MinPrice']
                if min_price < max_price_pp:
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
                    cache_results.append(advencha)
            next_friday = next_friday + datetime.timedelta(days=7)
            next_sunday = next_sunday + datetime.timedelta(days=7)
            count += 1          
        cache_results.sort(key=operator.attrgetter("price"), reverse=False)
        return cache_results
    
    def browse_cache(self, search_params):
        i = 0 
        cache_results = list()
        while i < len(search_params.departure_dates):
            departure_date = search_params.departure_dates[i]
            return_date = search_params.return_dates[i]
            try:    
                result = self.flights_cache.get_cheapest_quotes(
                                market=self.market,
                                currency=self.currency,
                                locale=self.locale,
                                originplace=search_params.origin,
                                destinationplace=search_params.destination,
                                outbounddate=departure_date.strftime('%Y-%m-%d'),
                                inbounddate=return_date.strftime('%Y-%m-%d')
                                ).parsed
            except Exception:
                print('ERROR: Could not access browse cache')
                continue
            cache_results.append(result)
            i += 1
        return cache_results
    
    #TODO Use this. How to return results though?
    #Either as is, then parse 'Quotes'
    #or compile a CacheAdventure object with results
    def browse_cache_by_route(self, search_params):
        i = 0 
        cache_results = dict()
        while i < len(search_params.departure_dates):
            departure_date = search_params.departure_dates[i]
            return_date = search_params.return_dates[i]
            try:    
                result = self.flights_cache.get_cheapest_price_by_route(
                                market=self.market,
                                currency=self.currency,
                                locale=self.locale,
                                originplace=search_params.origin,
                                destinationplace=search_params.destination,
                                outbounddate=departure_date.strftime('%Y-%m-%d'),
                                inbounddate=return_date.strftime('%Y-%m-%d')
                                ).parsed
            except Exception:
                print('ERROR: Could not access browse cache by route')
                continue
            if i == 0:
                #First iteration, set the carriers, currencies and places
                cache_results['Carriers'] = list()
                cache_results['Currencies'] = result['Currencies']
                cache_results['Places'] = list()
                cache_results['Quotes'] = list()
                cache_results['Routes'] = list()
            found_cheap_quote = False
            for quote in result['Quotes']:
                if quote['MinPrice'] <= search_params.max_price_pp and quote['Direct'] == True:
                    cache_results['Quotes'].append(quote)
                    found_cheap_quote = True
            for route in result['Routes']:
                if 'Price' in route and route['Price'] <= search_params.max_price_pp:
                    cache_results['Routes'].append(route)
            if found_cheap_quote == True:
                cache_results = self.append_if_doesnt_exist(target=cache_results, source=result, key_name='Carriers', attribute_name='CarrierId')
                cache_results = self.append_if_doesnt_exist(target=cache_results, source=result, key_name='Places', attribute_name='PlaceId')
            i += 1
        return cache_results

    #Needs exact destination place
    def browse_cache_by_date(self, search_params):
        i = 0 
        cache_results = list()
        while i < len(search_params.departure_dates):
            departure_date = search_params.departure_dates[i]
            return_date = search_params.return_dates[i]
            try:    
                result = self.flights_cache.get_cheapest_price_by_date(
                                market=self.market,
                                currency=self.currency,
                                locale=self.locale,
                                originplace=search_params.origin,
                                destinationplace=search_params.destination,
                                outbounddate=departure_date.strftime('%Y-%m-%d'),
                                inbounddate=return_date.strftime('%Y-%m-%d')
                                ).parsed
            except Exception:
                print('ERROR: Could not access browse cache by date')
                continue
            cache_results.append(result)
            i += 1
        return cache_results
    
    def browse_cache_grid_by_date(self, search_params):
        return
    
     
    def retrieve_adventure_details(self, adventure, adults, max_price_pp, earliest_dept_time, latest_dept_time, earliest_ret_time, latest_ret_time):     
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
        except Exception:
            print("ERROR: Exception trying to access Flights API:\n")
            print(str(Exception))
        try:
            itineraries = result['Itineraries']
            legs = result['Legs']
            places = result['Places']
            agents = result['Agents']
        except:
            print("ERROR: Could not establish itineraries from the flights result\n")
            return list()
        cheap_itineraries = list()
        for itinerary in itineraries:
            pricing = itinerary['PricingOptions']
            for price in pricing:
                full_price = price['Price']
                if full_price <= (max_price_pp*adults):
                    flight_agents = list()
                    for single_agent in price['Agents']:
                        flight_agents.append(self.get_agent_details(agents, single_agent))
                    #agents = price['Agents']
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
                else:
                    break
            break
        return cheap_itineraries