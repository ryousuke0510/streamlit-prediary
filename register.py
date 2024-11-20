import streamlit as st
from streamlit_folium import st_folium  # 地図の描画をするモジュール
import folium                           # 地図の生成をするモジュール
import googlemaps
import datetime
#import sqlite
#from sqlite import insert_schedule
import manage_page

from datetime import datetime
from zoneinfo import ZoneInfo
# 現地時間のタイムゾーンを指定（例: 日本時間）
local_now = datetime.now(ZoneInfo("Asia/Tokyo")).date()

import os
from dotenv import load_dotenv

# .envファイルの読み込み
load_dotenv()

# Geocoding APIから現在位置を取得
gm = googlemaps.Client(
        key=os.environ["API_KEY"]
    )

def show_page():

    # 初期設定
    # DEFAULT_DATE = datetime.now()      # datetime.date 型で現在の日付を指定
    DEFAULT_TIME = datetime.time(0,0)    # datetime.time 型で時間を指定
    DEFAULT_LOCATION = ""
    location_input = DEFAULT_LOCATION    # 表示したい位置情報のラベルを文字列として設定

    st.markdown("# スケジュール登録")  # st.markdownを使ってタイトルを表示

    # 日付入力
    date_input = st.date_input("日付を入力してください")
    # 時間入力
    time_input = st.time_input("時間を入力してください", DEFAULT_TIME)

    # 目的地入力
    user_input = st.text_input("目的地を入力してください（例：大阪駅）")
    # ユーザからの入力があった場合
    if user_input:
        # ユーザからの入力が空でなかった場合
        if user_input != DEFAULT_LOCATION:
            # 場所（名称）をセッションに保存
            if "location_input" not in st.session_state:
                st.session_state.location_input = user_input
            else:
                st.session_state.location_input = user_input
        
            st.session_state.last_clicked = False

            geocode_result = gm.geocode(st.session_state.location_input)
            # ユーザが入力した目的地が見つかった場合
            if geocode_result:
                res = geocode_result[0]['geometry']['location']
            else:
                st.warning("場所が見つかりませんでした。入力を確認してください。")
                res = None

            # Geocoding APIから返答があった場合
            if res:
                location = [res['lat'], res['lng']]
            
            update_location(location)  # 地図を表示or更新

        # 登録内容の確認＆データベースへの登録
        data_list = [date_input, time_input, st.session_state.location_input]
        confirm_data(data_list)

""" 
地図を更新する関数
@param location_input(list型[float?緯度, float?経度])
"""
def update_location(location):
    # 目的地の緯度と経度、最後の更新処理がクリック入力かキーボード入力かの状態の保存
    st.session_state.destination = location
    if "location_latitude" not in st.session_state:
        st.session_state.location_latitude = location[0]
    if "location_longitude" not in st.session_state:
        st.session_state.location_longitude = location[1]
    if "last_clicked" not in st.session_state:
        st.session_state.last_clicked = False

    # 地図の描画の準備（地図オブジェクトmの作成）
    m = folium.Map(
        location=st.session_state.destination,  # 地図の場所
        zoom_start=16,                          # 初期拡大率
        attr='Folium map'                       # 地図の属性
    )

    # マーカーの描画の準備
    folium.Marker(
        st.session_state.destination,         # 指定場所にマーカーを追加
        tooltip=str(st.session_state.destination), # マーカーにカーソルを合わせたときに表示されるテキスト
        icon=folium.Icon(color="blue")        # アイコンの追加と色の設定
    ).add_to(m)

    # 地図上でクリックイベントを取得&描画
    output = st_folium(m, width=350, height=275)
    st.write("目的地を更新しました")

    # ユーザーが地図上をクリックした場合の処理
    if output and 'last_clicked' in output and output['last_clicked']:
        st.session_state.last_clicked = True
        st.write(st.session_state.last_clicked)
        st.session_state.location_latitude, st.session_state.location_longitude = output['last_clicked']['lat'], output['last_clicked']['lng']

        # 新しい目的地を更新
        st.session_state.destination = [st.session_state.location_latitude, st.session_state.location_longitude]
        update_location(st.session_state.destination)


"""
内容確認＆登録
@param data_list(list型[date型:日付, time型:時間, list型:場所（名称）])
"""
def confirm_data(data_list):

    # データを格納
    date_input = data_list[0]
    time_input = data_list[1]
    location_input = data_list[2]
    
    # 日付，時間の状態をセッションに保存
    if "date_input" not in st.session_state:
        st.session_state.date_input = date_input
    if "time_input" not in st.session_state:
        st.session_state.time_input = time_input

    # 中央揃えのカラムを作成（3列中2番目）
    colum1, colum2, colum3 = st.columns([2, 2, 1])

    # 中央のカラムに登録内容確認ボタンを配置
    with colum2:
        st.button("登録内容確認", on_click=manage_page.button_confirm_change, key = "register_button", type="primary")