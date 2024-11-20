import streamlit as st
from streamlit_folium import st_folium  # 地図の描画をするモジュール
import folium                           # 地図の生成をするモジュール
import googlemaps
import datetime
#import sqlite
#from sqlite import insert_schedule
from register import update_location
import manage_page

from datetime import datetime as dt
from zoneinfo import ZoneInfo
# 現地時間のタイムゾーンを指定（例: 日本時間）
local_now = dt.now(ZoneInfo("Asia/Tokyo")).date()

import os
from dotenv import load_dotenv

# .envファイルの読み込み
load_dotenv()

def show_page():
    st.markdown("""
        <h1 style="text-align: center;">再登録</h1>
    """, unsafe_allow_html=True)

    # 日付入力
    new_date_input = st.date_input("日付を入力してください", local_now, st.session_state.date_input, key = 'new_date')
    # 時間入力
    new_time_input = st.time_input("時間を入力してください", st.session_state.time_input, key = 'new_time')
    # 目的地入力
    new_location_input = st.text_input("目的地を入力してください", st.session_state.location_input, key = 'new_location')
    
    if new_location_input != st.session_state.location_input:
        st.session_state.last_clicked = False

    # 入力内容をセッションに保存(更新される前に登録ボタンを押すと反映されない)
    st.session_state.date_input = new_date_input
    st.session_state.time_input = new_time_input
    st.session_state.location_input = new_location_input


    # 目的地を取得
    location = st.session_state.location_input

    # Google Maps APIを使用して住所を緯度経度に変換
    gmaps = googlemaps.Client(
            key=os.environ["API_KEY"]
        )

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
            location = [lat, lng]
            update_location(location)  # 地図を表示or更新
        else:
            st.error("住所の変換に失敗しました。正しい住所を入力してください。")
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")

    # 一行空ける
    st.write("")

    # 中央揃えのカラムを作成（3列中2番目）
    colum1, colum2, colum3 = st.columns([2, 2, 1])

    # 中央のカラムに登録内容確認ボタンを配置
    with colum2:
    # 登録ボタンが押されたら最終確認画面へ遷移
        st.button("登録内容確認",on_click=manage_page.button_registered_change, key = "register", type="primary")