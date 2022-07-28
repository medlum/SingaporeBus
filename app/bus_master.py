import json
import requests
import requests, json, folium, csv, math
from DataXY import coordData
from DataRoute import routeData
from folium.plugins import LocateControl
from pathlib import Path
from datetime import datetime

# ---- api connect bus route data ---- #
#lta_url = "http://datamall2.mytransport.sg/ltaodataservice/BusRoutes"
#
#headers = {"AccountKey": "DThSMrZZSdmUQjrFCDt3Ew==",
#           "accept": "application/json"}
#response = requests.request(method="get", url=lta_url, headers=headers)
#print(response.status_code)
#data = response.json()
##print(json.dumps(data, indent=4))
#rdata = data["value"]

# -----read bus route from csv ---- #
"""
fp = Path.cwd()/"bus_routes.csv"
with fp.open("r") as file:
    reader = csv.reader(file)
    next(reader)
    rdata = [i for i in reader]
"""


# ---- select bus route data by bus number ---- #
serv_num = "111"



def match(serv_num):
    # ---- match bus number to bustopcode to add coordinates ---- #
    serv_num_dat = [i for i in routeData if i[1] == serv_num]
    for i in range(len(coordData)):
        for j in range(len(serv_num_dat)):
            if serv_num_dat[j][5] in coordData[i][0]: # match busstop code
                serv_num_dat[j].extend(coordData[i][1:4]) # add lat, long and description

    # ---- select bus route data by bus stop ---- #
    # [5] busstop code [13] description
    serv_bus_dat = [[i[5], i[13]] for i in serv_num_dat]  

    # ---- extract coordinates for lines ---- #
    # [14] latitude [15] longitude
    points = [(i[14], i[15]) for i in serv_num_dat]

    return serv_num_dat, serv_bus_dat, points

# -------- api call to bus arrival real time -------- #

code = "09059"

def busarrival(code):

    # ---- api call ---- #
    url = f"http://datamall2.mytransport.sg/ltaodataservice/BusArrivalv2?BusStopCode={code}"
    headers = {"AccountKey": "DThSMrZZSdmUQjrFCDt3Ew==",
            "accept": "application/json"}
    response = requests.request(method="get", url=url, headers=headers)
    print(response.status_code)
    data = response.json()
    sdata = data["Services"] # [Services] contains arrival data

    return sdata


def busstoploc(serv_num_dat):
    # ---- retrieve coordinates from bustop code ---- #
    busstop_loc = [[i[14], i[15]] for i in serv_num_dat if code in i]
    return busstop_loc
    
# ---- map bus route data by bus number ---- #


m = folium.Map(location=busstop_loc[0], tiles="CartoDB positron",
               name="Light Map", zoom_start=13, attr="My Data")

LocateControl().add_to(m)


for i in serv_num_dat:
    loc = [i[14], i[15]] #latitude and longitude located index 14 and 15
    #custom_icon = folium.CustomIcon(icon_image='bus_icon.png', icon_size=(30, 30))
    folium.CircleMarker(
        location=loc, 
        color="grey",
        fill = True,
        fill_color = "grey",
        opacity=0.7,
        fill_opacity=0.7,
        tooltip=f'<p style="color:brown;font-size:10px;"> <strong>{i[13]}</strong> </p>',
        radius=8).add_to(m)

folium.PolyLine(points, 
                color = "red",
                weight = 10,
                opacity=0.3,
                smooth_factor=1).add_to(m)
#AntPath(points).add_to(m)

# ---- current time ---- #
curT = datetime.now().replace(microsecond=0)
curTT = str(curT.time())
current = datetime.strptime(curTT, "%H:%M:%S")
# ---- map selected bus stop ---- #

for i in sdata:
    arr = datetime.strptime(i["NextBus"]["EstimatedArrival"], '%Y-%m-%dT%H:%M:%S%z')
    arrTT = str(arr.time())
    arrival = datetime.strptime(arrTT, "%H:%M:%S")
    eta = arrival - current
    if str(eta).startswith("-"):
        eta = 0
    else:
        eta_floor = math.floor(eta.total_seconds()/60)

    if i["NextBus"]["Load"] == "SEA":

        folium.Marker(
            location=[i["NextBus"]["Latitude"], i["NextBus"]["Longitude"]],
            tooltip=folium.Tooltip(f"Bus {i['ServiceNo']} <br> {eta_floor} mins", permanent=True),
            icon=folium.Icon(color="green", icon="fa-solid fa-bus", prefix='fa')
            ).add_to(m)
    
    elif i["NextBus"]["Load"] == "SDA":

        folium.Marker(
            location=[i["NextBus"]["Latitude"], i["NextBus"]["Longitude"]],
            tooltip=folium.Tooltip(f"Bus {i['ServiceNo']} <br> {eta_floor} mins", permanent=True),
            icon=folium.Icon(color="red", icon="fa-solid fa-bus", prefix='fa')
        ).add_to(m)

    else:
        folium.Marker(
            location=[i["NextBus"]["Latitude"], i["NextBus"]["Longitude"]],
            tooltip=folium.Tooltip(
                f"Bus {i['ServiceNo']} <br> {eta_floor} mins", permanent=True),
            icon=folium.Icon(
                color="orange", icon="fa-solid fa-bus", prefix='fa')
        ).add_to(m)



    #tooltip=folium.Tooltip(f"Bus {i['ServiceNo']} <br> {eta_floor} mins", permanent=True)

    #popup=folium.Popup(f"Bus {i['ServiceNo']} <br> {eta_floor} mins", min_width=40, max_width=40, show=True),

folium.Marker(location=busstop_loc[0],
              icon=folium.Icon(color="blue", icon="fa-solid fa-briefcase", prefix='fa')
              ).add_to(m)

m.save("bsmap.html")
#jdat = json.dumps(data["value"], indent=4)
#print(jdat)



