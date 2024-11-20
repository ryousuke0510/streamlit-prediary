import streamlit as st
from streamlit_folium import st_folium
import folium
import googlemaps
import manage_page

import os
from dotenv import load_dotenv
# .envファイルの読み込み
load_dotenv()

def show_page():
    st.markdown("""
        <h1 style="text-align: center;">登録内容</h1>
    """, unsafe_allow_html=True)

    # 日時と時間
    st.markdown(f"""
        <div style="background-color: #e0f7fa; padding: 20px; border-radius: 5px;">
            <h3 style="text-align: center;">日時：{st.session_state.date_input}, {st.session_state.time_input}</h3>
            <h3 style="text-align: center;">目的地：{st.session_state.location_input}</h3>
            <h3 style="text-align: center;">上記内容で登録します</h3>
        </div>
    """, unsafe_allow_html=True)

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

    # 4列作成し、中央にボタンが来るように余白を調整
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])

    # 左のボタン
    with col2:
        st.button("はい", on_click=manage_page.button_register_yes_change, key="yes_button", type="primary")

    # 右のボタン
    with col3:
        st.button("いいえ", on_click=manage_page.button_register_no_change, key="no_button", type="primary")
