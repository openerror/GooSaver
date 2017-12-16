from time import time
#import gmplot, polyline

'''
    Contains all functions computing some sort of trip suggestion,
    hybrid of otherwise
'''

def publicTransitOnly(advice):
    '''
        Purpose: Retrieve info of a public transit only trip, for contrast
                 with the program's suggestions

                 advice: Google's API returns suggestions contained in a list;
                         advice is an entry in that list
    '''

    # "duration" for determining whether it's a short trip;
    # "steps", for in case it's a short trip and suggestions need to be displayed
    transitOnly_tripInfo = {}
    transitOnly_tripInfo["duration"] = advice['legs'][0]['duration']['value']
    transitOnly_tripInfo["steps"] = advice['legs'][0]['steps']

    return transitOnly_tripInfo


def optimize(advice, mapObj, uberObj, method = "duration"):
    '''
        Combine optimizeByTime and optimizeByLength, b/c there's much redundant code
        Possible values of mode: "time". "length"
        Change length -> duration, for clarity of meaning?
    '''
    # First, create the dict object that will be returned
    hybrid_tripInfo = dict(total_duration=0.0, uber_prices=[],
                           transit_line_connected="",
                           begin_station="",
                           end_station="",
                           final_leg_dist="")

    # Retrieve the latitudes and longitudes of origin and destination, for later use
    coordKeys = ('lat', 'lng')
    origin_c = [ advice['legs'][0]['start_location'][key] for key in coordKeys ]
    destination_c = [ advice['legs'][0]['end_location'][key] for key in coordKeys ]
    steps, durations, distances = mapObj.extractSteps(advice)


    if method.lower() == "duration":
        transit_duration = max(durations)
        transit_index = durations.index(transit_duration)
        transit_distance = distances[transit_index]
    elif method.lower() == "distance":
        transit_distance = max(distances)
        transit_index = distances.index(transit_distance)
        transit_duration = durations[transit_index]
    else:
        print("ERROR: Unknown optimization method specified. Aborting")
        return {}

    mode = mapObj.extractTransportMode(steps, transit_index)

    if mode == "WALKING":
        print("TODO: Use Uber to cover the walking segment if it exceeds a certain distance/time")
    else:
        # Extract info about the transit segment to which the user will connect
        transit_details = steps[transit_index]['transit_details']
        departLat, departLng = [ transit_details['departure_stop']['location'][c] for c in coordKeys ]
        arriveLat, arriveLng = [ transit_details['arrival_stop']['location'][c] for c in coordKeys ]

        replacement_est = uberObj.getPrices(origin_c, (departLat, departLng))

        # Compute the total durations as a list
        # There're more than one possible value, because wait times differ across Uber types
        uber_wait_duration = uberObj.getWaitTime(origin_c)
        uber_ride_duration = replacement_est[0]['duration'] #Same for all Uber types; quirk of Uber API
        afterUber_directions = mapObj.queryTrip((arriveLat, arriveLng), destination_c,
                                                time() + uber_ride_duration)
        afterUber_duration = afterUber_directions[0]['legs'][0]['duration']['value']

        total_duration = [(wait + uber_ride_duration + transit_duration + afterUber_duration) for wait in uber_wait_duration]
        
        # Find out how far the destination is, after getting off public transit
        dist_matrix = mapObj.gmaps.distance_matrix(steps[transit_index]['end_location'], 
                                                   steps[-1]['end_location'], 
                                                   mode = "walking")
        final_leg_dist = dist_matrix['rows'][0]['elements'][0]['distance']['text']
        
        # Testing: generating HTML file with Google Map
#        gmap = gmplot.GoogleMapPlotter(departLat, departLng, 15)
#        transit_trace = polyline.decode(steps[transit_index]['polyline']['points'])
#
#        lats = []; lngs = []
#        for coordinates in transit_trace:
#            lats.append(coordinates[0])
#            lngs.append(coordinates[1])
#
#        gmap.scatter(lats, lngs, marker = False)
#        gmap.scatter([origin_c[0], destination_c[0]], [origin_c[1], destination_c[1]])
#        gmap.draw("test.html")

        # Forming the dictionary for output!
        hybrid_tripInfo['total_duration'] = total_duration
        hybrid_tripInfo['begin_station'] = transit_details['departure_stop']['name']
        hybrid_tripInfo['end_station'] = transit_details['arrival_stop']['name']
        hybrid_tripInfo['uber_prices'] = [{product['localized_display_name']: product['estimate']} for product in replacement_est]
        hybrid_tripInfo['final_leg_dist'] = final_leg_dist
        
        if transit_details['line']['name'] in ["Metro Local Line", "Metro Rapid Line"]:
            hybrid_tripInfo['transit_line_connected'] = transit_details['line']['name'] + f" {transit_details['line']['short_name']}"
        else:
            hybrid_tripInfo['transit_line_connected'] = transit_details['line']['name']

    return hybrid_tripInfo
