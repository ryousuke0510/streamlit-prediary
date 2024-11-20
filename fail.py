import streamlit as st
import sqlite3
from streamlit_current_location import current_position

from PIL import Image

def show_page():
    # CSSを使って文字を中央に配置
    st.markdown(
        """
        <style>
        .center-text {
            display: flex;
            justify-content: center;
            font-size: 48px;
            font-weight: bold;
        }
        </style>
        <div class="center-text">失敗...</div>
        """,
        unsafe_allow_html=True
    )
    

    st.session_state["page"] = "home"
    
    # 画像ファイルを読み込む
    image = Image.open('fail.png')

    # Streamlitで画像を表示
    st.image(image, use_container_width=True)
