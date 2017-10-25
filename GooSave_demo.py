from datetime import datetime
from UberWrapper import UberWrapper
from MapWrapper import MapWrapper
from misc import printTime, printUberPrices, displayTrip
from methods import optimizeByLength, optimizeByTime

uber_token="wisG3tcaRLg2sFZ49g042Bi47RvoOgDWXs-avv8h"
google_key="AIzaSyD6n0hcRjovaiDrMOhgFuk4iGA7SjJOS0U"

def main(origin, destination, departAt = datetime.now()):
    # Create google and Uber objects
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
        # TODO: wrap relevant code in the functions optimize_time(), optimize_length
        # Find the longest segment --- by duration AND distance, respectively
        # Then, determine the mode of transport and duration of travel
        # If the two coincide, optimize by the former (an arbitary choice)
        
        for advice in end2end_directions:
            # First, display info regarding public-transit-only trip, for comparison
            end2end_duration = advice['legs'][0]['duration']['value']
            steps, durations, distances = mapObj.extractSteps(advice) 

            longestStepDuration = max(durations)
            longestStepIndex = durations.index(longestStepDuration)
            mode = mapObj.extractTransportMode(steps, longestStepIndex)
            
            print("Using only public transit, the entire trip takes {}.".format(printTime(end2end_duration)))
            print("Segment {} takes the longest, at {}, using {}.".format(longestStepIndex+1,
                                                                         printTime(longestStepDuration),
                                                                         mode))
            
            optimizeByLength(advice, mapObj, uberObj)
            print("\n")            
            optimizeByTime(advice, mapObj, uberObj)

    # __ Cost for UBER only __ #
    print("\nIn contrast, taking an Uber straight to the destination costs")
    end2end_est = uberObj.getPrices(origin_c, destination_c)
    printUberPrices(end2end_est)

    # DEBUG: return API queries for examination and understanding '''
    return end2end_directions

dirResult = main(origin = "University Regent, Los Angeles",
                 destination= "Hodori, Vermont Avenue, Los Angeles")
