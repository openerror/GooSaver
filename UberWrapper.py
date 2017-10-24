#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Custom wrappers for Uber API
"""

from uber_rides.session import Session
from uber_rides.client import UberRidesClient

class UberWrapper(object):
    def __init__(self, token):
        self.session = Session(server_token=token)
        self.client = UberRidesClient(self.session)
        
    def getPrices(self, origin, destination, seats=1):
        ''' origin, destination: tuples of (longtitude, latitude) 
        
            response contains a bunch of dict objects, each for an Uber product
            The low_estimate, high_estimate keys give the price
            'duration' key gives estimated time in secs
        '''
        
        response = self.client.get_price_estimates(start_latitude=origin[0],
                                              start_longitude=origin[1],
                                              end_latitude=destination[0],
                                              end_longitude=destination[1],
                                              seat_count=seats)
        estimate = response.json.get('prices')        
        return estimate
    
    def getWaitTime(self, origin, seats = 1):
        ''' origin, destination: tuples of (longtitude, latitude) '''
        
        response = self.client.get_pickup_time_estimates(origin[0], origin[1]).json
        waitTime = [product['estimate'] for product in response['times']]
        return waitTime