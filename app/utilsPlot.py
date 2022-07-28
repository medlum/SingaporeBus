
import folium, math
from folium.plugins import LocateControl, FloatImage
from folium.features import DivIcon
from datetime import datetime
from utils import *

def map_route(serv_num_dat, m):

    # plot bus route selected by bus service number
    for i in serv_num_dat:

        loc = [i[14], i[15]]  # latitude and longitude located index 14 and 15
        folium.CircleMarker(
            location=loc,
            color="grey",
            fill=True,
            fill_color="grey",
            opacity=0.7,
            fill_opacity=0.7,
            tooltip=f'<p style="color:DarkSlateGray;font-size:10px;"> {i[13]} </p>',
            radius=8).add_to(m)

def map_routeline(points, m):
    
    folium.PolyLine(points,
                    color="red",
                    weight=10,
                    opacity=0.3,
                    smooth_factor=1).add_to(m)

def map_busstop(sdata,current, m):
    #global eta

    # ---- map selected bus stop ---- #
    for i in sdata:

        # ---- convert bus arrival timestamp to time H:M:S ---- #
        arr = datetime.strptime(
            i["NextBus"]["EstimatedArrival"], '%Y-%m-%dT%H:%M:%S%z')
        arrTT = str(arr.time())
        arrival = datetime.strptime(arrTT, "%H:%M:%S")
        # find time interval between system and arrival time
        # current is system time from utils
        eta = arrival - current
        if str(eta).startswith("-"):  # handle display '- 1 day...' when arrival < current
            eta = "Arriving" 
        else:
            eta = f"{math.floor(eta.total_seconds()/60)} mins"  # find secs and round down
        
        if eta == "0 mins":
            eta = "Arriving"
        
        # ---- SEA - Seats Available, Marker = green ---- #
        if i["NextBus"]["Load"] == "SEA":
          
            folium.Marker(
                location=[i["NextBus"]["Latitude"], i["NextBus"]["Longitude"]],
                icon=folium.Icon(
                    color="green", icon="fa-solid fa-bus", prefix='fa')
            ).add_to(m)

            folium.Marker(
                location=[i["NextBus"]["Latitude"], i["NextBus"]["Longitude"]],
                icon=number_DivIcon(i['ServiceNo'], eta)
            ).add_to(m)


        # ---- SDA - Standing Available, Marker = red ---- #
        elif i["NextBus"]["Load"] == "SDA":

            folium.Marker(
                location=[i["NextBus"]["Latitude"], i["NextBus"]["Longitude"]],
                icon=folium.Icon(color="red", icon="fa-solid fa-bus", prefix='fa')
            ).add_to(m)

            folium.Marker(
                location=[i["NextBus"]["Latitude"], i["NextBus"]["Longitude"]],
                icon=number_DivIcon(i['ServiceNo'], eta)
            ).add_to(m)

        else:
            # ---- LSD - Limited Standing, Marker = "orange"---- #
            folium.Marker(
                location=[i["NextBus"]["Latitude"], i["NextBus"]["Longitude"]],
                icon=folium.Icon(
                    color="orange", icon="fa-solid fa-bus", prefix='fa')
            ).add_to(m)

            folium.Marker(
                location=[i["NextBus"]["Latitude"], i["NextBus"]["Longitude"]],
                icon=number_DivIcon(i['ServiceNo'], eta)
            ).add_to(m)

    #return eta


def map_selection(busstop_loc, m):

    # mark selection busstop
    folium.Marker(location=[busstop_loc[0], busstop_loc[1]],
                icon=folium.Icon(color="blue", icon="fa-solid fa-briefcase", prefix='fa')
                ).add_to(m)
    
    folium.Marker(location=[busstop_loc[0], busstop_loc[1]],
                  icon=DivIcon(
                    icon_size=(100,100),
                    icon_anchor=(90,60),
                    html=f'<p style="font-size: 12pt; color : DodgerBlue"> <strong> {busstop_loc[2]} </strong></p>'
                    )
                    ).add_to(m)

    # place legend on map
    #FloatImage('assets/legend.png', bottom=0, left=0).add_to(m)

