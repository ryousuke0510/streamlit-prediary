import streamlit as st
from streamlit_folium import st_folium  # 地図の描画をするモジュール
import folium                           # 地図の生成をするモジュール
import googlemaps
import datetime
#import sqlite
#from sqlite import insert_schedule
import manage_page

# add
import sqlite3

def insert_schedule(date, time, location, latitude, longitude, achievement, userid):
    # SQLite3データベースに接続
    db_path = "database.db"  # データベースファイルのパス
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO schedules (date, time, location, latitude, longitude, achievement, userid)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (date, time, location, latitude, longitude, achievement, userid))
    
    conn.commit()
    conn.close()


def show_page():
    # 登録内容の情報表示
    st.markdown(f"""
        <div style="background-color: #f1f8e9; padding: 20px; border-radius: 5px;">
            <h3 style="text-align: center;">下記内容で登録されました</h3>
            <h4 style="text-align: center;">日時: {st.session_state.date_input}, {st.session_state.time_input}</h4>
            <h4 style="text-align: center;">目的地: {st.session_state.location_input}</h4>
        </div>
    """, unsafe_allow_html=True)

    # 目的地を取得
    location = st.session_state.location_input

    # Google Maps APIを使用して住所を緯度経度に変換
    gmaps = googlemaps.Client(key="AIzaSyB9jQ01kfY8jre3vl7X_pl9qJ7pVCmhquA")  # APIキーを設定
    try:
        geocode_result = gmaps.geocode(location)
        if geocode_result:
            # 地図の最終更新時がクリックであった場合
            if st.session_state.last_clicked:
                lat = st.session_state.location_latitude
                lng = st.session_state.location_longitude

            # 地図の最終更新時がキーボード入力であった場合
            else:
                lat = geocode_result[0]['geometry']['location']['lat']
                lng = geocode_result[0]['geometry']['location']['lng']
            
            # 地図の生成
            map_center = [lat, lng]
            map_obj = folium.Map(location=map_center, zoom_start=15)
            folium.Marker(location=map_center, popup=f"目的地: {location}").add_to(map_obj)

            # 地図を描画
            st_folium(map_obj, width=350, height=275)
        else:
            st.error("住所の変換に失敗しました。正しい住所を入力してください。")
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")

    # 一行空ける
    st.write("")

    # 登録するデータを格納
    date_input = date_to_string(st.session_state.date_input)  # 日付
    time_input = time_to_string(st.session_state.time_input)  # 時間
    location_input = st.session_state.location_input          # 場所（名称）
    latitude = st.session_state.location_latitude             # 緯度
    longitude = st.session_state.location_longitude           # 経度
    achievement = False                                       # 初期値として未達成に設定
    userid = st.session_state["id"]                           # ユーザID

    # データベースのスケジュールテーブルに登録
    st.write(date_input, time_input, location_input, latitude, longitude, achievement, userid)
    insert_schedule(date_input, time_input, location_input, latitude, longitude, achievement, userid)


# date型を文字列に変換 
def date_to_string(date_input):
    # 数字のみの文字列に変換 (例: "YYYYMMDD"形式)
    date_str = date_input.strftime("%Y%m%d")
    return date_str


# time型を文字列に変換
def time_to_string(time_input):
    # 数字のみの文字列に変換 (例: "HHMM"形式)
    time_str = time_input.strftime("%H%M")
    return time_str