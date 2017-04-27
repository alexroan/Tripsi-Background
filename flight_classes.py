'''
Created on 26 Sep 2016

@author: Alex Roan
'''
import datetime


class SearchParameters:
    
    def __init__(self, origin, destination, max_price_pp, weekly_departure_day, weekly_return_day, weeks_ahead, earliest_dept_time, latest_dept_time, earliest_ret_time, latest_ret_time, adults):
        self.origin = origin
        self.destination = destination
        self.max_price_pp = max_price_pp
        self.departure_dates = self.get_list_of_dates(day_in_week=weekly_departure_day, weeks_ahead=weeks_ahead)
        self.return_dates = self.get_list_of_dates(day_in_week=weekly_return_day, weeks_ahead=weeks_ahead)        
        self.earliest_dept_time = earliest_dept_time
        self.latest_dept_time = latest_dept_time
        self.earliest_ret_time = earliest_ret_time
        self.latest_ret_time = latest_ret_time
        self.adults = adults
        
    def get_list_of_dates(self, day_in_week, weeks_ahead):
        dates = list()
        start_date = datetime.datetime.now()
        d = start_date
        i = 0
        while i < weeks_ahead:
            dates.append(self.next_weekday(date=d, weekday=day_in_week))
            d = d + datetime.timedelta(days=7)
            i+=1
        return dates
        
    def next_weekday(self, date, weekday):
        days_ahead = weekday - date.weekday()
        if days_ahead < 0: # Target day already happened this week
            days_ahead += 7
        return date + datetime.timedelta(days_ahead)


class FlightItinerary:
    
    def __init__(self, 
                 price, 
                 agents, 
                 link, 
                 adults,
                 dept_from, 
                 dept_time, 
                 dept_duration, 
                 dept_stops, 
                 dept_arrive_location, 
                 dept_arrive_time,
                 ret_from, 
                 ret_time, 
                 ret_duration,
                 ret_stops,
                 ret_arrive_location,
                 ret_arrive_time
                 ):
        self.price = price
        self.agents = agents
        self.link = link
        self.adults = adults
        self.dept_from = dept_from
        self.dept_time = dept_time
        self.dept_duration = dept_duration
        self.dept_stops = dept_stops
        self.dept_arrive_location = dept_arrive_location
        self.dept_arrive_time = dept_arrive_time
        self.ret_from = ret_from
        self.ret_time = ret_time
        self.ret_duration = ret_duration
        self.ret_stops = ret_stops
        self.ret_arrive_location = ret_arrive_location
        self.ret_arrive_time = ret_arrive_time
        
    def __str__(self):
        s="Departing From "+str(self.dept_from)+" To "+str(self.dept_arrive_location)+"\n"
        s+="Leaving at "+str(self.dept_time)+" and landing at "+str(self.dept_arrive_time)+" ("+str(self.dept_duration)+" mins with "+str(self.dept_stops)+" stops)\n"
        s+="Returning From "+str(self.ret_from)+" To "+str(self.ret_arrive_location)+"\n"
        s+="Leaving at "+str(self.ret_time)+" and landing at "+str(self.ret_arrive_time)+" ("+str(self.ret_duration)+" mins with "+str(self.ret_stops)+" stops)\n"
        s+="Total price for "+str(self.adults)+" adults = "+str(self.price)+"\n"
        s+=str(self.link)+"\n\n"
        return s
        

class CacheAdventure:
    
    def __init__(self, price, direct, dept_date, dept_place, dept_iata, dept_carriers, ret_date, ret_place, ret_iata, ret_carriers, cache_date):
        self.price = price
        self.direct = direct
        self.cache_date = cache_date
        
        self.departure_date = dept_date
        self.departure_place = dept_place
        self.departure_iata = dept_iata
        self.departure_carriers = dept_carriers
           
        self.return_date = ret_date
        self.return_place = ret_place
        self.return_iata = ret_iata
        self.return_carriers = ret_carriers
    
    def __str__(self):
        s = str(self.departure_place)+" to "+str(self.return_place)+"\n"        
        s += "Price: "+str(self.price)+"\n"
        s += "Direct: "+str(self.direct)+"\n"
        s += "Departure Date: "+str(self.departure_date)+"\n"
        s += "Departure Place: "+str(self.departure_place)+"\n"
        s += "Departure IATA: "+str(self.departure_iata)+"\n"
        s += "Departure Carriers:\n"
        for dc in self.departure_carriers:
            s += "\t"+str(dc)+"\n"
        s += "Return Date: "+str(self.return_date)+"\n"
        s += "Return From: "+str(self.return_place)+"\n"
        s += "Return IATA: "+str(self.return_iata)+"\n"
        s += "Return Carriers:\n"
        for rc in self.return_carriers:
            s += "\t"+str(rc)+"\n"
        s += "Cache Date: "+str(self.cache_date)+"\n"
        return s
    
    def basic_str(self):
        return str(self.departure_place)+" to "+str(self.return_place)+"\t"+str(self.departure_date)+"-"+str(self.return_date)+" Price: £"+str(self.price)
    