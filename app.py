import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pickle 

from MapWrapper import MapWrapper
from UberWrapper import UberWrapper
from methods import optimize
from datetime import datetime

from misc import printTime

uber_token="wisG3tcaRLg2sFZ49g042Bi47RvoOgDWXs-avv8h"
google_key="AIzaSyD6n0hcRjovaiDrMOhgFuk4iGA7SjJOS0U"
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
                html.Div(id = "output")
        ])
    
@app.callback(
    Output("output", "children"),
    [Input("submit_query", "n_clicks")],
     [State("origin", "value"),
      State("dest", "value")]
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

if __name__ == '__main__':
    app.run_server()