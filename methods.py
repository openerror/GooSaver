from misc import printUberPrices, printTime
from time import time

def optimizeByTime(advice, mapObj, uberObj):
        # Retrieve the latitudes and longitudes of origin and destination, for later use
        coordKeys = ('lat', 'lng')
        origin_c = [ advice['legs'][0]['start_location'][key] for key in coordKeys ]
        destination_c = [ advice['legs'][0]['end_location'][key] for key in coordKeys ]
        
        steps, durations, distances = mapObj.extractSteps(advice)
        maxTime = max(durations); maxTimeIndex = durations.index(maxTime)
        mode = mapObj.extractTransportMode(steps, maxTimeIndex)

        if mode == "WALKING":
            print("You're gonna walk to ... !")
            
        elif mode != "WALKING":
            transitDetails = steps[maxTimeIndex]['transit_details']

            departLat, departLng = [ transitDetails['departure_stop']['location'][c] for c in coordKeys ]
            arriveLat, arriveLng = [ transitDetails['arrival_stop']['location'][c] for c in coordKeys ]
            departStation = transitDetails['departure_stop']['name']

            print("Riding Uber to the beginning of segment {}, {}, costs".format(maxTimeIndex+1,
                                                                                  departStation))
            replacement_est = uberObj.getPrices(origin_c, (departLat, departLng))
            printUberPrices(replacement_est)

            # Determine transit durations BEFORE and AFTER Uber segment
            uberDuration = replacement_est[0]['duration'] #Same for all Uber types
            waitDuration = uberObj.getWaitTime(origin_c)

            afterUber_result = mapObj.queryTrip((arriveLat, arriveLng),
                                                destination_c,
                                                time() + uberDuration)

            afterUberDuration = afterUber_result[0]['legs'][0]['duration']['value']

            totalDuration = [wait+uberDuration+maxTime+afterUberDuration for wait in waitDuration]
            print("All in all, the hybrid trip takes at least {}.".format(printTime(min(totalDuration)))) 

def optimizeByLength(advice, mapObj, uberObj):
        # Retrieve the latitudes and longitudes of origin and destination, for later use
        coordKeys = ('lat', 'lng')
        origin_c = [ advice['legs'][0]['start_location'][key] for key in coordKeys ]
        destination_c = [ advice['legs'][0]['end_location'][key] for key in coordKeys ]
        
        steps, durations, distances = mapObj.extractSteps(advice)
        maxDistance = max(distances); maxDistanceIndex = distances.index(maxDistance)
        maxDistanceDuration = durations[ maxDistanceIndex ]        
        
        mode = mapObj.extractTransportMode(steps, maxDistanceIndex)
        
        print("The longest trip (by distance) is segment %i" %(maxDistanceIndex+1))
        
        if mode != "WALKING":
                transitDetails = steps[maxDistanceIndex]['transit_details']

                departLat, departLng = [ transitDetails['departure_stop']['location'][c] for c in coordKeys ]
                arriveLat, arriveLng = [ transitDetails['arrival_stop']['location'][c] for c in coordKeys ]
                departStation = transitDetails['departure_stop']['name']

                print("Riding Uber to the beginning of segment {}, {}, costs".format(maxDistanceIndex+1,
                                                                                      departStation))
                
                replacement_est = uberObj.getPrices(origin_c, (departLat, departLng))
                printUberPrices(replacement_est)

                # Determine transit durations BEFORE and AFTER Uber segment
                uberDuration = replacement_est[0]['duration'] #Same for all Uber types
                waitDuration = uberObj.getWaitTime(origin_c)

                afterUber_result = mapObj.queryTrip((arriveLat, arriveLng),
                                                    destination_c,
                                                    time() + uberDuration)

                afterUberDuration = afterUber_result[0]['legs'][0]['duration']['value']

                totalDuration = [wait+uberDuration+maxDistanceDuration+afterUberDuration for wait in waitDuration]
                print("All in all, the hybrid trip takes at least {}.".format(printTime(min(totalDuration))))