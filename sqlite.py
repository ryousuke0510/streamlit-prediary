import sqlite3

# SQLite3データベースに接続
db_path = "database.db"  # データベースファイルのパス
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# ユーザテーブル作成
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE, -- ユーザネーム
    password TEXT NOT NULL,        -- パスワード
    nickname TEXT NOT NULL,        -- ニックネーム
    level INTEGER NOT NULL         -- レベル
)
''')


# スケジュールテーブル作成
cursor.execute('''
CREATE TABLE IF NOT EXISTS schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,           -- 年月日:"20241019"
    time TEXT NOT NULL,           -- 時刻:"1730"
    location TEXT NOT NULL,       -- 大阪駅
    latitude REAL NOT NULL,       -- 緯度
    longitude REAL NOT NULL,      -- 経度
    achievement BOOLEAN NOT NULL, -- 達成
    userid INTEGER NOT NULL       -- ユーザid
)
''')

users = [
    ("user1", "pass1", "いぬ", 1),
    ("user2", "pass2", "ねこ", 2),
    ("user3", "pass3", "とり", 1),
    ("user4", "pass4", "さる", 3),
    ("user5", "pass5", "とら", 2),
    ("user6", "pass6", "ごりら", 5),
    ("user7", "pass7", "きりん", 4),
    ("user8", "pass8", "かば", 1),
    ("user9", "pass9", "リス", 2),
    ("user10", "pass10", "きつね", 1),
    
]

# サンプルユーザーの挿入（必要に応じて）
cursor.executemany('''
INSERT INTO users (username, password, nickname, level)
VALUES (?, ?, ?, ?)
''', users)

schedules = [
    ("20241019", "1730", "大阪駅", 34.702, 135.495, True, 1),
    ("20241020", "1400", "京都駅", 35.011, 135.768, False, 2),
    ("20241021", "1030", "神戸駅", 34.690, 135.195, True, 3),
    ("20241022", "1600", "奈良駅", 34.683, 135.832, False, 1),
    ("20241023", "1200", "天王寺駅", 34.646, 135.513, True, 2),
    ("20241024", "1800", "梅田駅", 34.704, 135.498, False, 3),
    ("20241025", "0900", "新大阪駅", 34.733, 135.500, True, 1),
    ("20241026", "1500", "三宮駅", 34.696, 135.195, True, 2),
    ("20241027", "1700", "高槻駅", 34.843, 135.617, False, 3),
    ("20241028", "1100", "茨木駅", 34.813, 135.568, True, 1),
    ("20241029", "2000", "西宮駅", 34.737, 135.341, False, 2),
    ("20241106", "2100", "西宮駅", 34.737, 135.341, True, 2),
    ("20241106", "1000", "西宮駅", 34.737, 135.341, True, 2),
    ("20241106", "2000", "西宮駅", 34.737, 135.341, False, 2),
    ("20241106", "2000", "西宮駅", 34.737, 135.341, True, 1),
    ("20241106", "2000", "西宮駅", 34.737, 135.341, False, 1),
]

# スケジュールの挿入（必要に応じて）
cursor.executemany('''
INSERT INTO schedules (date, time, location, latitude, longitude, achievement, userid)
VALUES (?, ?, ?, ?, ?, ?, ?)
''', schedules)


# 変更を保存
conn.commit()

# データベース接続を閉じる
conn.close()