import streamlit as st
import sqlite3
import manage_page
from streamlit_folium import st_folium
import folium

from datetime import datetime
from zoneinfo import ZoneInfo
# 現地時間のタイムゾーンを指定（例: 日本時間）
local_now = datetime.now(ZoneInfo("Asia/Tokyo")).date()

def change_date_format(date):
    str_date = str(date)
    return str_date[0:4] + str_date[5:7] + str_date[8:10]

def change_time_format(time):
    str_time = str(time)
    return str_time[0:2] + ":" + str_time[2:4]

def show_page():
    # 日付入力
    selected_date = st.date_input('Input date', local_now)
    formatted_date = change_date_format(selected_date)  # 日付をフォーマット

    # SQLite3データベースに接続
    db_path = "database.db"  # データベースファイルのパス
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    userid = st.session_state["id"]
        
    # 現在のユーザのidで一致するスケジュールのみを取得
    cursor.execute(
        "SELECT time, location, latitude, longitude, achievement FROM schedules WHERE date = ? AND userid = ?",
        (formatted_date, userid)
    )
    schedules = cursor.fetchall()
    
    # データベースを閉じる
    conn.close()

    # スケジュールの表示
    if schedules:
        # forループで複数のボタンを生成
        for idx, (time, location, latitude, longitude, achievement) in enumerate(schedules):
            if achievement == True:
                st.button(f"{change_time_format(time)}   {location} 達成済み", key=f"button_{idx}", args=(idx, formatted_date, time, location, latitude, longitude), use_container_width=True, type="primary")  # 関数に渡す引数
            elif achievement == False:
                st.button(f"{change_time_format(time)}   {location}", key=f"button_{idx}", on_click=manage_page.button_home_change, args=(idx, formatted_date, time, location, latitude, longitude), use_container_width=True)  # 関数に渡す引数
    else:
        st.write("スケジュールはありません")
    
    if st.session_state["current_latitude"] != None:
        # 地図の初期位置
        initial_location = [st.session_state["current_latitude"], st.session_state["current_longitude"]]
        m = folium.Map(
            location=initial_location,
            zoom_start=16,
            attr='Folium map'
        )
        folium.Marker(
                    [st.session_state["current_latitude"], st.session_state['current_longitude']],
                    #popup=location.address,
                    tooltip="現在地",
                    icon=folium.Icon(color="red")
                ).add_to(m)
        # 地図の中心を入力した場所に移動
        m.location = st.session_state["current_latitude"], st.session_state['current_longitude']
        m.zoom_start = 16
        
        st_folium(m, width=350, height=275)