import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

# データベース接続用関数
def connect_db():
    return sqlite3.connect('database.db')

# レベル上位3人を取得する関数
def get_top_level_users():
    conn = connect_db()
    cursor = conn.cursor()
    query = """
    SELECT nickname, level FROM users
    ORDER BY level DESC
    LIMIT 3;
    """
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return pd.DataFrame(data, columns=["Nickname", "Level"])

# 最新の日で目標を達成した回数上位3人を取得する関数
def get_recent_top_achievers():
    conn = connect_db()
    cursor = conn.cursor()
    # 最新の日付を取得
    cursor.execute("SELECT MAX(date) FROM schedules WHERE achievement = 1;")
    latest_date = cursor.fetchone()[0]

    # 最新の日付での達成回数上位3人
    query = """
    SELECT u.nickname, COUNT(s.achievement) AS achievements
    FROM users u
    JOIN schedules s ON u.id = s.userid
    WHERE s.achievement = 1 AND s.date = ?
    GROUP BY u.id
    ORDER BY achievements DESC
    LIMIT 3;
    """
    cursor.execute(query, (latest_date,))
    data = cursor.fetchall()
    conn.close()
    return pd.DataFrame(data, columns=["Nickname", "Achievements"])

# 過去7日間の目標達成回数上位3人を取得する関数
def get_top_achievers_last_7_days():
    conn = connect_db()
    cursor = conn.cursor()
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y%m%d')
    query = """
    SELECT u.nickname, COUNT(s.achievement) AS achievements
    FROM users u
    JOIN schedules s ON u.id = s.userid
    WHERE s.achievement = 1 AND s.date >= ?
    GROUP BY u.id
    ORDER BY achievements DESC
    LIMIT 3;
    """
    cursor.execute(query, (seven_days_ago,))
    data = cursor.fetchall()
    conn.close()
    return pd.DataFrame(data, columns=["Nickname", "Achievements"])

# Streamlitのページ表示
def show_page():
    st.markdown("# ランキング表示")
    
    # レベル上位3人のランキング表示
    st.subheader("レベル上位3人")
    top_level_df = get_top_level_users()
    st.table(top_level_df)

    # 最新の日での達成回数上位3人のランキング表示
    st.subheader("最新の日で目標を達成した回数上位3人")
    recent_achievers_df = get_recent_top_achievers()
    st.table(recent_achievers_df)

    # 過去7日間での達成回数上位3人のランキング表示
    st.subheader("過去7日間で目標を達成した回数上位3人")
    top_achievers_df = get_top_achievers_last_7_days()
    st.table(top_achievers_df)