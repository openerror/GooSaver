from datetime import date, datetime
from UberWrapper import UberWrapper
from MapWrapper import MapWrapper

uber_token="wisG3tcaRLg2sFZ49g042Bi47RvoOgDWXs-avv8h"
google_key="AIzaSyD6n0hcRjovaiDrMOhgFuk4iGA7SjJOS0U"


def main(origin, destination, departAt = datetime.now()):
    # Create google object and make a query
    mapObj = MapWrapper(google_key)
    uberObj = UberWrapper(uber_token)
    
    directions_result = mapObj.queryTrip(origin,
                                         destination,
                                         departAt)
    print("Google has returned {} trip suggestions".format(len(directions_result)))

#    for trip in directions_result:
#        # Compute sth for each suggestion
#        countLegs(trip)

    # Display the monetary and time cost for taking an Uber
    origin_c = mapObj.geocode(origin)
    destination_c = mapObj.geocode(destination)
    
    estimates = uberObj.getPrices(origin_c, destination_c)
    product = uberObj.getTime(origin_c)
    
    return directions_result, product, estimates

dirResult,product, estimates = main(origin = "University of Southern California", 
                                    destination="Pasedena City College")
