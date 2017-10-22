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

    def optimize_length(self, advice):
        pass

    def optimize_time(self, advice):
        pass

    def geocode(self, place):
        ''' place is a string (address or building name etc) '''

        geocode_result = self.gmaps.geocode(place)
        lat = geocode_result[0]['geometry']['location']['lat']
        lng = geocode_result[0]['geometry']['location']['lng']

        return (lat, lng)

    def queryTrip(self, origin, destination, departAt, preferRail=False):
        if preferRail:
            mode = ["rail"]
        else:
            mode = ["rail", "bus"]

        result = self.gmaps.directions(origin, destination, mode = "transit",
                                       transit_mode = mode,
                                       alternatives = False,
                                       departure_time = departAt)
        return result

    def extractSteps(self, advice):
        steps = advice['legs'][0]['steps']
        stepDurations = [s['duration']['value'] for s in steps]
        return steps, stepDurations

    def extractTransportMode(self, steps, index):
        '''
            Extract from a specified step the mode of commute (walking / public transit)

            'steps' is a list extracted from the advice['legs'][index]['steps']
            'steps' contains detailed information on each segment of the trip
                - where/when to begin/stop
                - transfer instructions (with human readable text)
                - the line of transit service used
        '''

        s = steps[index]
        try:
            transit_details = s['transit_details']
            mode = transit_details['line']['name']

            # If bus, must append additional info
            if mode == "Metro Local Line":
                mode += ' (' + transit_details['line']['short_name'] + ')'
            return mode

        except KeyError:
            mode = "WALKING"
            return mode
