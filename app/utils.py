import folium
import requests,math
from DataXY import coordData
from DataRoute import routeData
from datetime import datetime
import datetime as dt
from folium.features import DivIcon
import streamlit as st
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
#serv_num = "111"

def match(serv_num):
    # ---- match bus number to bustopcode to add coordinates ---- #
    serv_num_dat = [i for i in routeData if i[1] == serv_num]
    for i in range(len(coordData)):
        for j in range(len(serv_num_dat)):
            if serv_num_dat[j][5] in coordData[i][0]:  # match busstop code
                # add lat, long and description
                serv_num_dat[j].extend(coordData[i][1:4])

    # ---- select bus route data by bus stop ---- #
    # [5] busstop code [13] description
    serv_bus_dat = [[i[5], i[13]] for i in serv_num_dat]

    # ---- extract coordinates for lines ---- #
    # [14] latitude [15] longitude
    points = [(i[14], i[15]) for i in serv_num_dat]

    return serv_num_dat, serv_bus_dat, points

# -------- api call to bus arrival real time -------- #

#code = "09059"
def busarrival(code):
    # ---- api call ---- #
    url = f"http://datamall2.mytransport.sg/ltaodataservice/BusArrivalv2?BusStopCode={code}"
    headers = {"AccountKey": st.secrets["LTA_APIKEY"],
               "accept": "application/json"}
    response = requests.request(method="get", url=url, headers=headers)
    print(response.status_code)
    data = response.json()
    sdata = data["Services"]  # [Services] contains arrival data

    return sdata


def matchbusarrival(sdata, serv_num, current):

    global eta, eta2, eta3

    for i in sdata:
        
        if i["ServiceNo"] == serv_num:
            print(i["ServiceNo"])
            arr = datetime.strptime(i["NextBus"]["EstimatedArrival"], '%Y-%m-%dT%H:%M:%S%z')
            arr2 = datetime.strptime(i["NextBus2"]["EstimatedArrival"], '%Y-%m-%dT%H:%M:%S%z')
            arr3 = datetime.strptime(i["NextBus3"]["EstimatedArrival"], '%Y-%m-%dT%H:%M:%S%z')
            arrTT = str(arr.time())
            arrTT2 = str(arr2.time())
            arrTT3 = str(arr3.time())
            arrival = datetime.strptime(arrTT, "%H:%M:%S")
            arrival2 = datetime.strptime(arrTT2, "%H:%M:%S")
            arrival3 = datetime.strptime(arrTT3, "%H:%M:%S")
            # find time interval between system and arrival time
            # current is system time from utils
            eta = arrival - current
            eta2 = arrival2 - current
            eta3 = arrival3 - current
            
            # handle display '- 1 day...' when arrival < current
            if str(eta).startswith("-"):
                eta = "Arriving"
            else:
                # find secs and round down
                eta = f"{math.floor(eta.total_seconds()/60)} mins"

            if str(eta2).startswith("-"):
                eta2 = "Arriving"
            else:
                # find secs and round down
                eta2 = f"{math.floor(eta2.total_seconds()/60)} mins"

            if str(eta3).startswith("-"):
                eta3 = "Arriving"
            else:
                # find secs and round down
                eta3 = f"{math.floor(eta3.total_seconds()/60)} mins"

            if eta == "0 mins":
                eta = "Arriving"

            if eta2 == "0 mins":
                eta2 = "Arriving"

            if eta3 == "0 mins":
                eta3 = "Arriving"

            return eta, eta2, eta3


# ---- retrieve coordinates from bustop code ---- #

def busstoploc(code, serv_num_dat):

    busstop_loc = [[i[14], i[15], i[13]] for i in serv_num_dat if code in i]
    busstop_loc = [item for sublist in busstop_loc for item in sublist]
    return busstop_loc

# ---- find system time ---- #
def currentTime():

    curT = datetime.now().replace(microsecond=0)
    curTT = str(curT.time())
    current = datetime.strptime(curTT, "%H:%M:%S")
    current = current + dt.timedelta(hours=8)

    return current

# ---- create a 'numbered' icon---- #

def number_DivIcon(number, eta):
    icon = DivIcon(
        icon_size=(90, 90),
        icon_anchor=(20, 60),
        html=f'<p style="font-size: 10pt; color : DarkSlateGray"> <strong> Bus {number} <br> <br> <br> {eta} </strong></p>'
    )
    return icon
