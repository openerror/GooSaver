### "GooSaver" Transit Suggestion Tool

#### Rationale and User Cases
Ever complained about how slow public transport is in LA, but couldn't bring yourself to take that expensive ride-sharing trip? Then GooSaver may be your next best friend :)

GooSaver works by suggesting how you might connect to public transport using Uber. In particular, the app aims to get you to the longest public transit trip as quickly as possible – which entails the use a private car.

Here is a test case for within Los Angeles, measured at 5:30pm on a Sunday. About 15-20 minutes are saved, and now you can read during the trip!

1. University of Southern California -> Pasadena Convention Center

![alt text](UserCase1")

#### Possible Further Developments
It's not that we prefer Uber over other services, but Uber's API is the most accessible of all from Python. When possible, we would like to incorporate e.g. Lyft, too.

Also, right now the map is displaying public-transit-only suggestions from Google. While they are useful for comparison to GooSaver's *text* output, ideally we would like to see it describe the trip suggested by GooSaver instead.
