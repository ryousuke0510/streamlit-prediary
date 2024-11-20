import streamlit as st
from streamlit_folium import st_folium  # 地図の描画をするモジュール
import folium                           # 地図の生成をするモジュール
import googlemaps
import datetime
#import sqlite
#from sqlite import insert_schedule
#from register import update_location
import manage_page

import os
from dotenv import load_dotenv

# .envファイルの読み込み
load_dotenv()

def show_page():
    st.markdown("""
        <h1 style="text-align: center;">再登録</h1>
    """, unsafe_allow_html=True)

    # 日付入力
    new_date_input = st.date_input("日付を入力してください", st.session_state.date_input, key = 'new_date')
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