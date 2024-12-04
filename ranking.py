import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
# import matplotlib.pyplot as plt
import altair as alt    #pythonの可視化データライブラリ,st.altair_chartっていう関数がある

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
    today = datetime.now().strftime('%Y%m%d')
    query = """
    SELECT u.nickname, COUNT(s.achievement) AS true_count
    FROM users u
    JOIN schedules s ON u.id = s.userid
    WHERE s.achievement = 1 AND s.date = ?
    GROUP BY u.id
    ORDER BY true_count DESC
    LIMIT 3;
    """
    cursor.execute(query, (today,))
    data = cursor.fetchall()
    conn.close()
    if not data:
        return pd.DataFrame([{"Nickname": "該当者なし", "Achievements": 0}])
    return pd.DataFrame(data, columns=["Nickname", "True Count"])

# 過去7日間の目標達成回数上位3人を取得する関数
def get_top_achievers_last_7_days():
    conn = connect_db()
    cursor = conn.cursor() #SQLクエリを実行するためのもの
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y%m%d')
    query = """
    SELECT u.nickname, COUNT(s.achievement) AS true_count
    FROM users u
    JOIN schedules s ON u.id = s.userid
    WHERE s.achievement = 1 AND s.date >= ? 
    GROUP BY u.id
    ORDER BY true_count DESC
    LIMIT 3;
    """
    #ここでは、WHERE s.date >= ? という条件を使って、指定された日付（ここでは start_date、つまり30日前）以降のデータを選択しています。
    cursor.execute(query, (seven_days_ago,))
    data = cursor.fetchall()
    conn.close()
    if not data:
        return pd.DataFrame([{"Nickname": "該当者なし", "Achievements": 0}])
    return pd.DataFrame(data, columns=["Nickname", "True Count"])

# 過去1ヶ月間の一週間ごとの達成回数を上位3人について取得する関数
def get_weekly_achievements_top_users():
    conn = connect_db()
    cursor = conn.cursor() #カーソルオブジェクトとは、Pythonのデータベースモジュール(例えばsqlite3)で使用されるオブジェクト。データベースとの対話を管理するためのインターフェース

    # 過去1か月分の範囲
    today = datetime.now()
    start_date = today - timedelta(days=30)
    start_date_str = start_date.strftime('%Y%m%d')

    # ユーザーごとの目標達成回数を取得
    query = """
    SELECT u.nickname, s.date, COUNT(s.achievement) AS true_count
    FROM users u
    JOIN schedules s ON u.id = s.userid
    WHERE s.achievement = 1 AND s.date >= ?
    GROUP BY u.id, s.date
    ORDER BY true_count DESC;
    """
    cursor.execute(query, (start_date_str,)) #execute:SQL分の実行
    data = cursor.fetchall() #データベースからクエリ結果を取得する。結果全部の行とか、一行だけとかいろいろ種類がある。
    conn.close()

    # データをDataFrameに変換
    df = pd.DataFrame(data, columns=["Nickname", "Date", "True Count"])

    # 日付をdatetime型に変換
    df["Date"] = pd.to_datetime(df["Date"], format='%Y%m%d')

    # **True Countを数値型に変換**
    df["True Count"] = pd.to_numeric(df["True Count"], errors="coerce")

    # 週ごとに集計
    df["Week"] = df["Date"].dt.to_period("W").apply(lambda r: r.start_time)
    weekly_df = df.groupby(["Nickname", "Week"])["True Count"].sum().reset_index()

    # 上位3人のユーザーを取得
    top_users = weekly_df.groupby("Nickname")["True Count"].sum().nlargest(3).index
    top_weekly_df = weekly_df[weekly_df["Nickname"].isin(top_users)]

    return top_weekly_df

# Streamlitのページ表示
def show_page():
    st.markdown("# 🎯 ランキング表示")
    st.write("以下はユーザーの達成状況に基づくトップ3のランキングです。")

    # # レベル上位3人のランキング表示
    # st.markdown("## 🏅 レベル上位3人")
    # top_level_df = get_top_level_users()
    # st.markdown("### **レベルランキング**")
    # st.write("**トップのレベルを誇るユーザーたち**")
    # st.table(top_level_df)

    st.markdown("## 🏅 レベル上位3人")
    top_level_df = get_top_level_users() #これってどんな中身？Nickname:Nの後半の:Nって何？
    if not top_level_df.empty:
        chart = alt.Chart(top_level_df).mark_bar().encode(
            x=alt.X("Nickname:N", title="ユーザー名"),
            y=alt.Y("Level:Q", title="レベル"),
            color="Nickname:N"
        ).properties(
            width=800,
            height=400,
            title="レベル上位3人"
        )
        st.altair_chart(chart, use_container_width=True)


    # 最新の日で目標を達成した回数上位3人のランキング表示
    # st.markdown("## 📅 最新の日で目標を達成した回数上位3人")
    # recent_achievers_df = get_recent_top_achievers()
    # st.markdown("### **最新の日での目標達成者**")
    # st.write("**今日達成した回数が最も多いユーザーたち**")
    # st.table(recent_achievers_df)

    st.markdown("## 📅 最新の日で目標を達成した回数上位3人")
    recent_achievers_df = get_recent_top_achievers()
    if not recent_achievers_df.empty:
        chart = alt.Chart(recent_achievers_df).mark_bar().encode(
            x=alt.X("Nickname:N", title="ユーザー名"),
            y=alt.Y("True Count:Q", title="達成回数"),
            color="Nickname:N"
        ).properties(
            width=800,
            height=400,
            title="最新の日で目標を達成した回数上位3人"
        )
        st.altair_chart(chart, use_container_width=True)

    # 過去7日間での達成回数上位3人のランキング表示
    # st.markdown("## 🗓️ 過去7日間で目標を達成した回数上位3人")
    # top_achievers_df = get_top_achievers_last_7_days()
    # st.markdown("### **過去7日間で最も目標を達成したユーザーたち**")
    # st.write("**過去1週間で目標達成回数が最も多いユーザーたち**")
    # st.table(top_achievers_df)

    st.markdown("## 🗓️ 過去7日間で目標を達成した回数上位3人")
    top_achievers_df = get_top_achievers_last_7_days()
    if not top_achievers_df.empty:
        chart = alt.Chart(top_achievers_df).mark_bar().encode(
            x=alt.X("Nickname:N", title="ユーザー名"),
            y=alt.Y("True Count:Q", title="達成回数"),
            color="Nickname:N"
        ).properties(
            width=800,
            height=400,
            title="過去7日間で目標を達成した回数上位3人"
        )
        st.altair_chart(chart, use_container_width=True)


# # Streamlitのページ表示
# def show_page():
    st.markdown("# 🎯 過去1ヶ月の目標達成回数")

    # 週ごとの達成回数を取得
    weekly_achievements_df = get_weekly_achievements_top_users()

    # データが存在する場合
    if not weekly_achievements_df.empty:
        # Altairを使った棒グラフの作成
        chart = alt.Chart(weekly_achievements_df).mark_bar().encode(
            x=alt.X("Week:T", title="週", axis=alt.Axis(format="%Y-%m-%d")),
            y=alt.Y("True Count:Q", title="達成回数"),
            color=alt.Color("Nickname:N", title="ユーザー名"),
            column=alt.Column("Nickname:N", title="ユーザー"),
            tooltip=["Nickname:N", "Week:T", "True Count:Q"]
        ).properties(
            width=800,
            height=400,
            title="過去1ヶ月間の目標達成回数（週別、上位3人）"
        )

        st.altair_chart(chart, use_container_width=True)
    else:
        st.write("データがありません。")