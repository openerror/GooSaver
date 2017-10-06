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
        ''' origin, destination: tuples of (longtitude, latitude) '''
        
        response = self.client.get_price_estimates(start_latitude=origin[0],
                                              start_longitude=origin[1],
                                              end_latitude=destination[0],
                                              end_longitude=destination[1],
                                              seat_count=seats)
        
        ''' Below are a bunch of dict objects 
            The low_estimate, high_estimate keys give the price
            'duration' key gives estimated time in secs
        '''
        
        estimate = response.json.get('prices')
        uberPool = estimate[0]
        uberX = estimate[1]
#        uberEspanol = estimate[2]
#        uberSelect = estimate[3]
#        uberXL = estimate[4]
#        uberBlack = estimate[5]
#        uberSUV = estimate[6]
#        uberLUX = estimate[7]
#        uberAssist = estimate[8]
#        uberWAV = estimate[9]

        print('UberPOOL costs {}. Duration: {}'.format(uberPool['estimate'], uberPool['duration']))
        print('UberX costs {}. Duration: {}'.format(uberX['estimate'], uberX['duration']))
        
        return estimate
        
    def getTime(self, origin):
        response = self.client.get_products(origin[0], origin[1])
        products = response.json.get('products')
        
        return products