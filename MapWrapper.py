#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Custom wrappers for Google Maps API
"""

import googlemaps
from datetime import date, datetime

class MapWrapper(object):
    def __init__(self, key):
        self.key = key
        self.gmaps = googlemaps.Client(key)
    
    def geocode(self, place):
        ''' place is a string (address or building name etc) ''' 
        
        geocode_result = self.gmaps.geocode(place)
        lat = geocode_result[0]['geometry']['location']['lat']
        lng = geocode_result[0]['geometry']['location']['lng']
        return (lat, lng)
    
    def queryTrip(self, origin, destination, departAt):
        result = self.gmaps.directions(origin,
                                  destination,
                                  mode = "transit",
                                  transit_mode = "rail",
                                  departure_time = departAt)
        return result
        
    def countLegs(self, direction_results):
        print("Google has given {} suggestions".format(len(direction_results)))
        
        for suggestion in direction_results:
            leg_data = suggestion["legs"]
            eta_date = date.fromtimestamp(leg_data[-1]["arrival_time"]["value"])
            eta_time_text = leg_data[-1]["arrival_time"]["text"]
        
            eta_time_value = leg_data[-1]["arrival_time"]["value"]
            dep_time_value = leg_data[0]["departure_time"]["value"]
            travel_duration = eta_time_value - dep_time_value
        
            print("\nTrip consists of {} legs".format(len(leg_data)))
            print("Estimated arrival time: {} {}".format(eta_date, eta_time_text))
            print("Estimated travel duration: {:.3f} hours".format(travel_duration/3600))
