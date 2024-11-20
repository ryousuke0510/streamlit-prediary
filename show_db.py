import sqlite3

# SQLite3データベースに接続
db_path = "database.db"  # データベースファイルのパス
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# usersテーブルの内容を取得
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

# 結果を表示
for row in rows:
    print(row)
    
# usersテーブルの内容を取得
cursor.execute("SELECT * FROM schedules")
rows = cursor.fetchall()

# 結果を表示
for row in rows:
    print(row)

# データベース接続を閉じる
conn.close()
