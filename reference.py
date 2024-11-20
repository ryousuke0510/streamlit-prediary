import streamlit as st
import sqlite3
from streamlit_current_location import current_position
import math
import manage_page
from streamlit_folium import st_folium
import folium


def change_time_format(time):
    str_time = str(time)
    return str_time[0:2] + ":" + str_time[2:4]

def cal_distance(target_latitude, target_longitude):
    
    LAT = 111.11111111
    LON = 111.11111111 * math.cos(math.radians(35))
    CIRCLE_DISTANCE = 0.6
    #print(LON)
    
    distance = math.sqrt((LAT*(target_latitude-st.session_state["current_latitude"])) ** 2 + (LON*(target_longitude-st.session_state["current_longitude"])) ** 2)
    
    #print(f"distance:{distance}")
    
    if distance <= CIRCLE_DISTANCE:
        return True
    else:
        return False
    

def show_page():
    
    # 位置情報と時間情報を表示
    with st.container():
        st.metric("時刻", change_time_format(st.session_state["time"]))
        st.metric("場所", st.session_state["location"])
    
    # 地図の初期位置
    initial_location = [st.session_state["destination_latitude"], st.session_state["destination_longitude"]]
    m = folium.Map(
        location=initial_location,
        zoom_start=16,
        attr='Folium map'
    )
    folium.Marker(
                [st.session_state["destination_latitude"], st.session_state['destination_longitude']],
                #popup=location.address,
                tooltip="現在地",
                icon=folium.Icon(color="red")
            ).add_to(m)
    # 地図の中心を入力した場所に移動
    m.location = st.session_state["destination_latitude"], st.session_state['destination_longitude']
    m.zoom_start = 16
    
    st_folium(m, width=350, height=275)
    
        
    # 目的地到着ボタン
    st.button("目的地到着！", on_click=manage_page.button_reference_change, key="arrive_button", use_container_width=True, type="primary")
    