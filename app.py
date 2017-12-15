import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from MapWrapper import MapWrapper
from UberWrapper import UberWrapper
from methods import optimize
from datetime import datetime

from misc import printTime

# Set up the external APIs
uber_token = "wisG3tcaRLg2sFZ49g042Bi47RvoOgDWXs-avv8h"
google_key = "AIzaSyBoShQRjZZ7gJeix0CeNghXsVKyoi0DaLs"
gmapObj = MapWrapper(google_key)
uberObj = UberWrapper(uber_token)

#___Code begins below___#
text_style = dict(color="#444", fontFamily="sans-serif", fontWeight=300)
newline = html.P("\n")
                  
app = dash.Dash()
app.layout = html.Div([
                html.H2(id = "welcome", children = "Welcome to GooSaver!", style = text_style),
                html.P("Please enter the origin and destination below", style=text_style),
                dcc.Input(id='origin', value='Origin here', type="text"),
                newline,
                dcc.Input(id='dest', value='Destination here', type="text"),
                html.Button(id="submit_query", children="Obtain results"),
                html.Div(id = "output"),
                newline,
                html.Iframe(id = "map", 
                            src = f"file://test.html",
                            width = 640,
                            height = 480)
        ])
    
@app.callback(
    Output("output", "children"),
    [Input("submit_query", "n_clicks")],
     [State("origin", "value"),
      State("dest", "value"),
     ]
    )
def parse_hybrid(click, origin, destination):
    ''' In production code, of course we will make a function call that 
        returns a dict object ''' 
    
    # Load a dict --- from file or from API calls
    advice = gmapObj.queryTrip(origin, destination, departAt = datetime.now())
    tripInfo = optimize(advice[0], gmapObj, uberObj, method = "distance")
    
    # Extract the necessary features and give them easy names
    min_duration = printTime( min(tripInfo['total_duration']) )
    transit_line = tripInfo['transit_line_connected']
    begin_station = tripInfo['begin_station']
    end_station = tripInfo['end_station']
    uber_prices = tripInfo['uber_prices']
            
    return html.Div([
                html.H3("GooSaver Trip Duration: {}\n".format(min_duration)),
                html.P("Take Uber and connect to {} @ {}\n".format(transit_line, begin_station)),
                html.Div("Get off at {}, ... \n\n".format(end_station)),
                html.Div([
                            html.H3("Uber Cost"),
                            html.Ul("\t Pool: {}".format(uber_prices[0]['POOL'])),
                            html.Ul("\t UberX {}".format(uber_prices[1]['uberX']))
                        ])
            ])

@app.callback(
        Output("map", "src"),
        [Input("submit_query", "n_clicks")],
        [State("origin", "value"), State("dest", "value")]  
        )     
def paintMap(click, origin, destination):
    origin_queryStr = ""
    for item in origin.split():
        origin_queryStr += item + "+"
        
    dest_queryStr = ""
    for item in destination.split():
        dest_queryStr += item + "+"
        
    return f"https://www.google.com/maps/embed/v1/directions?key={google_key}&mode=transit&origin={origin_queryStr[:-1]}&destination={dest_queryStr[:-1]}" 

if __name__ == '__main__':
    app.run_server()