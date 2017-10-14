from time import time
from datetime import datetime
from UberWrapper import UberWrapper
from MapWrapper import MapWrapper
from misc import printTime, printUberPrices, displayTrip

uber_token="wisG3tcaRLg2sFZ49g042Bi47RvoOgDWXs-avv8h"
google_key="AIzaSyD6n0hcRjovaiDrMOhgFuk4iGA7SjJOS0U"

def main(origin, destination, departAt = datetime.now()):
    # Create google object and make a query
    mapObj = MapWrapper(google_key)
    uberObj = UberWrapper(uber_token)
    
    # Retrieve the latitudes and longitudes of origin and destination, for later use
    origin_c = mapObj.geocode(origin)
    destination_c = mapObj.geocode(destination)
    
    # ___ Google: query for directions  ___ #
    end2end_directions = mapObj.queryTrip(origin, destination, departAt,
                                          preferRail=False)
    
    assert len(end2end_directions) > 0, "Google returns no suggestions. Exiting."
    print("Google has returned {} trip suggestion(s)\n".format(len(end2end_directions)))
    
    # Analyze the results, and recommend any trips that take less than 30 mins
    shortTripFound = False
    
    for advice in end2end_directions:
        totalDuration = advice['legs'][0]['duration']['value']
        if totalDuration <= 2100:
            print("Trip lasting less than 35 mins found.")
            displayTrip(advice); shortTripFound = True
            print("\n")
    
    if shortTripFound:
        return
    else:
        # Find the longest segment. 
        # Then, determine the mode of transport and duration of travel
        for advice in end2end_directions:
            end2end_duration = advice['legs'][0]['duration']['value']
            steps, stepDurations = mapObj.extractSteps(advice) 
            
            longestStepDuration = max(stepDurations)
            longestStepIndex = stepDurations.index(longestStepDuration)
            mode = mapObj.extractTransportMode(steps, longestStepIndex)
                        
            print("Using only public transit, the entire trip takes {}.".format(printTime(end2end_duration)))
            print("Segment {} takes the longest, at {}, using {}.".format(longestStepIndex+1,
                                                                         printTime(longestStepDuration),
                                                                         mode))
            if mode != "WALKING":
                transitDetails = steps[longestStepIndex]['transit_details']
                coordKeys = ('lat', 'lng')
                
                departLat, departLng = [transitDetails['departure_stop']['location'][c] for c in coordKeys]
                arriveLat, arriveLng = [transitDetails['arrival_stop']['location'][c] for c in coordKeys]
                departStation = transitDetails['departure_stop']['name']
                                
                print("Riding Uber to the beginning of segment {}, {}, costs".format(longestStepIndex+1,
                                                                                      departStation))
                replacement_est = uberObj.getPrices(origin_c, (departLat, departLng))
                printUberPrices(replacement_est)
                
                # Determine transit durations BEFORE and AFTER Uber segment
                uberDuration = replacement_est[0]['duration'] #Same for all Uber types
                waitDuration = uberObj.getWaitTime(origin_c)
                                
                afterUber_result = mapObj.queryTrip((arriveLat, arriveLng), 
                                                    destination, 
                                                    time() + uberDuration)
                
                afterUberDuration = afterUber_result[0]['legs'][0]['duration']['value']
                
                totalDuration = [wait+uberDuration+longestStepDuration+afterUberDuration for wait in waitDuration]
                print("All in all, the hybrid trip takes at least {}.".format(printTime(min(totalDuration))))

    # __ Cost for UBER only __ #
    print("\nIn contrast, taking an Uber straight to the destination costs")
    end2end_est = uberObj.getPrices(origin_c, destination_c)
    printUberPrices(end2end_est)
    
    # DEBUG: return API queries for examination and understanding ''' 
    return end2end_directions

dirResult = main(origin = "University Regent, Los Angeles", 
                 destination="Pasadena City College, CA")
