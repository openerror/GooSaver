#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Miscellaneous functions required by GooSaver
"""

def displayTrip(advice):
    ''' Display nicely to the user a single suggestion from Google 
        Input: an unaltered dict object in the list returned by queryTrip()
            
        Duration, boarding point, where to get off
    '''
        
    #Specification: duration, boarding station, where to get off
    duration = advice['legs'][0]['duration']['value'] # in seconds
    steps = advice['legs'][0]['steps']                # steps is a list of dicts
        
    print("Trip duration: {}".format(printTime(duration)))
        
    for singleStep in steps:
        html_instructions = singleStep['html_instructions']
            
        if singleStep['travel_mode'] == "WALKING":
            print("\t", html_instructions)
        elif singleStep['travel_mode'] == "TRANSIT":
            headsign = singleStep['transit_details']['headsign']
            num_stops = singleStep['transit_details']['num_stops']
            print("\t", html_instructions)
            print("\t", "Head sign: {}. Number of stops {}".format(headsign, num_stops))

def printTime(secs):
    ''' Print a duration in secs nicely
        format: [] h [] min
        If less than one hour, omit the h part
    '''
    
    s = float(secs)
    if s < 3600.:
        m = int(s/60)
        output = '{} min'.format(m)
    else:
        h = int(s/3600)
        m = int((s - h * 3600)/60)
        output = '{} h {} min'.format(h, m)
    
    return output

def printUberPrices(estimate):
    ''' print out nicely the results returned by UberWrapper.getPrices() '''
    
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
    
    print('\t (POOL) {}. Duration: {}'.format(uberPool['estimate'], 
                                              printTime(uberPool['duration'])))
    print('\t (UberX) {}. Duration: {}'.format(uberX['estimate'], 
                                               printTime(uberX['duration'])))
