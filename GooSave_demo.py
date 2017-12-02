from datetime import datetime
from UberWrapper import UberWrapper
from MapWrapper import MapWrapper
from misc import printUberPrices, displayTrip, printTime
from methods import optimize, publicTransitOnly

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
    end2end_directions = mapObj.queryTrip(origin, destination, departAt, preferRail=False)

    assert len(end2end_directions) > 0, "Google returns no suggestions. Exiting."
    print("Google has returned {} trip suggestion(s)\n".format(len(end2end_directions)))

    # Analyze the results, and recommend any trips that take less than 30 mins    
    for advice in end2end_directions:
        transitOnly_tripInfo = publicTransitOnly(advice)
        transitOnly_duration = transitOnly_tripInfo["duration"]
        
        # Encourages use of public transit only, for shorter trips
        if (transitOnly_duration <= 2100):
            print("Trip lasting less than 35 mins found.")
            return dirResult, transitOnly_tripInfo
        else:
            hybrid_tripInfo = optimize(advice, mapObj, uberObj, method = "distance")
            print("If you use only public transit, the entire trip takes {}.".format(printTime(transitOnly_duration)))

    # __ Cost for UBER only __ #
    print("\nIn contrast, taking an Uber straight to the destination costs")
    end2end_est = uberObj.getPrices(origin_c, destination_c)
    printUberPrices(end2end_est)

    # DEBUG: return API queries for examination and understanding '''
    return end2end_directions, hybrid_tripInfo 

dirResult, hybrid_tripInfo = main(origin = "University of Southern California, Los Angeles",
                                  destination= "Hodori, Vermont Avenue, Los Angeles")