import streamlit as st
import sqlite3
from streamlit_current_location import current_position
import manage_page
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
        <div class="center-text">成功！</div>
        """,
        unsafe_allow_html=True
    )
    
    # バルーンの演出
    st.balloons()

    # セッション状態をリセット
    
    st.session_state["page"] = "home"

    # 画像ファイルを読み込む
    image = Image.open('success.png')

    # Streamlitで画像を表示
    st.image(image, use_container_width=True)
    
    # その他の処理（スケジュールデータベースの更新やレベルアップ）
    increase_user_level(st.session_state["id"])
    

def increase_user_level(user_id):
    try:
        # SQLite3データベースに接続
        db_path = "database.db"  # データベースファイルのパス
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 現在のレベルを取得
        cursor.execute("SELECT level FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchone()

        if result is None:
            print(f"ユーザID {user_id} は存在しません。")
            return

        current_level = result[0]

        # レベルを1増やす
        new_level = current_level + 1
        cursor.execute("UPDATE users SET level = ? WHERE id = ?", (new_level, user_id))

        # 変更を保存
        conn.commit()
        #print(f"ユーザID {user_id} のレベルを {current_level} から {new_level} に更新しました。")
        conn.close()

    except sqlite3.Error as e:
        print(f"エラーが発生しました: {e}")
