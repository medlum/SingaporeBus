from folium import FeatureGroup
from utils import *
from utilsPlot import *
from utilsStream import *
import streamlit as st
import streamlit_folium
from streamlit_folium import folium_static
from folium.plugins import LocateControl, FloatImage, FeatureGroupSubGroup
from PIL import Image
from folium.features import DivIcon

st.set_page_config(
    page_title='Bus ',
    page_icon=':shark:',
    layout="wide",
    menu_items={"About": "Data is updated on one minute interval"}
)
set_bg("assets/wallpaper.jpg")
head()

serv_num = st.sidebar.text_input("Enter Bus No. :")
serv_num_dat, serv_bus_dat, points = match(serv_num)
busStopCode = [i[5] for i in serv_num_dat]
busStopDesr = [i[13] for i in serv_num_dat]
selectstop = st.sidebar.selectbox(label="Select a Bus Stop", options=busStopDesr)

code = ""
for index, stop in enumerate(busStopDesr):
    if stop == selectstop:
        code = busStopCode[index]
  


if code != "":

    #serv_num = "111"
    serv_num_dat, serv_bus_dat, points = match(serv_num)
    #code = "09059"
    sdata = busarrival(code)
    busstop_loc = busstoploc(code, serv_num_dat)
    current = currentTime()
    eta, eta2, eta3 = matchbusarrival(sdata, serv_num, current)

    m = folium.Map(location=[busstop_loc[0], busstop_loc[1]],
                    tiles="CartoDB positron",
                    name="Light Map",
                    zoom_start=14)

    map_route(serv_num_dat, m)
    map_routeline(points, m)
    map_busstop(sdata, current, m)
    map_selection(busstop_loc, m)
    
   
    

    #st.header(f"Arrival Information for Bus Number {serv_num}")
    #b1, b2, b3 = container.columns(3)

    col1, col2 = st.columns([1,1])
    
    with col1:
        st.write(
            f"<p style='text-align: left; color:GreenYellow'> Current Time: {current.time()} </p>", unsafe_allow_html=True)
        st.write(
            f'<p style="color:GhostWhite;font-size:40px;"> Arrival {serv_num} </p>', unsafe_allow_html=True)
        st.metric(label=f"Next Timing", value=f"\U0001F55B {eta}")
        st.metric(label=f"Subsequent Timing", value=f"\U0001F567 {eta2}")
        st.metric(label=f"Subsequent Timing", value=f"\U0001F550 {eta3}")
        with st.expander("See explanation"):
            image = Image.open("assets/legend_h3.png")
            st.image(image=image)

    with col2:
        #st.write(
        #    f'<p style="color:LightSteelBlue;font-size:30px;"> Bus No. {serv_num} Route </p>', unsafe_allow_html=True)

        streamlit_folium.st_folium(m, width=500,height=500)



    


