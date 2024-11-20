import streamlit as st
import math
import sqlite3
from datetime import datetime

from zoneinfo import ZoneInfo

DIFFERENCE_TIME = 30

# 距離に関する目標達成判定
def cal_distance(target_latitude, target_longitude):
    
    LAT = 111.11111111
    LON = 111.11111111 * math.cos(math.radians(35))
    CIRCLE_DISTANCE = 1.0
    #print(LON)
    
    distance = math.sqrt((LAT*(target_latitude-st.session_state["current_latitude"])) ** 2 + (LON*(target_longitude-st.session_state["current_longitude"])) ** 2)
    
    #print(f"distance:{distance}")
    
    if distance <= CIRCLE_DISTANCE:
        #print("TRUE")
        return True
    else:
        #print("FALSE")
        return False

# 時間に関する目標達成判定
def check_time(scheduled_time):
    # 現在時刻を取得
    current_time = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%H%M")
    
    # 形式を分単位に変更（例：02:30 -> 150）
    minutes_current_time = int(current_time[0:2]) * 60 + int(current_time[2:4])
    miniutes_scheduled_time = int(scheduled_time[0:2]) * 60 + int(scheduled_time[2:4])
    
    #print(minutes_current_time)
    #print(miniutes_scheduled_time)
    #print(abs(minutes_current_time - miniutes_scheduled_time))
    
    # 30分以内の場合成功
    if abs(minutes_current_time - miniutes_scheduled_time) <= DIFFERENCE_TIME:
        return True
    else:
        return False


# ページ切り替え用の関数
def flag_change(key):
    # 選択されたページによってセッションステートのpageを変更する
    selection = st.session_state[key]
    #print(selection)
    if selection == "ホーム":
        st.session_state["page"] = "home"
    elif selection == "登録":
        st.session_state["page"] = "register"
    elif selection == "ランク":
        st.session_state["page"] = "ranking"
    elif selection == "履歴":
        st.session_state["page"] = "history"        
        

def button_home_change(idx, date, time, location, latitude, longitude):
    #print(location)
    #print(time)
    #print(st.session_state["page"])
    if st.session_state['page'] == "home":
        st.session_state['page'] = "reference"
        st.session_state["date"] = date
        st.session_state["time"] = time
        st.session_state["location"] = location
        st.session_state["destination_latitude"] = latitude
        st.session_state["destination_longitude"] = longitude
        #print(st.session_state["location"])
        #st.session_state["option"] = "other"
        
        
def button_reference_change():
    
    #if st.session_state['page'] == "reference":    
    # SQLite3データベースに接続
    db_path = "database.db"  # データベースファイルのパス
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    date = st.session_state["date"]
    time = st.session_state["time"]
    location = st.session_state["location"]

    # スケジュールを取得
    # 日付と時刻を使用してスケジュールを取得
    cursor.execute("SELECT id, latitude, longitude FROM schedules WHERE date = ? AND time = ? AND location = ?", (date, time, location))
    schedules = cursor.fetchall()

    if schedules:
        for id, latitude, longitude in schedules:
            #print(f"Latitude: {latitude}, Longitude: {longitude}")
            if cal_distance(latitude, longitude) and check_time(time):
                st.session_state['page'] = "success"
                # レコードの achievement を True に更新
                cursor.execute('''
                    UPDATE schedules
                    SET achievement = 1
                    WHERE id = ?
                ''', (id,))

                # 変更を保存
                conn.commit()
            
            else:
                st.session_state['page'] = "fail"
                
    # データベースを閉じる
    conn.close()
        
        
def button_register_change():
    if st.session_state['page'] == "register":
        return 
                    
def button_confirm_change():
    # 確認画面へ遷移
    st.session_state['page'] = "confirm"

def button_register_yes_change():
    # 登録内容表示画面へ遷移
    st.session_state['page'] = "registered"
    
def button_register_no_change():
    st.session_state['page'] = "reconfirm"
    
def button_registered_change():
    # 再確認画面へ遷移
    st.session_state['page'] = "confirm"  