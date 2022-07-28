import requests
import json
import folium
from DataXY import coord_info
from folium.plugins import AntPath, BeautifyIcon, LocateControl

# ---- api connect bus route data ---- #
lta_url = "http://datamall2.mytransport.sg/ltaodataservice/BusStops"

headers = {"AccountKey": "DThSMrZZSdmUQjrFCDt3Ew==",
           "accept": "application/json"}
response = requests.request(method="get", url=lta_url, headers=headers)
print(response.status_code)
data = response.json()
print(json.dumps(data, indent=4))
print(len(data["value"]))