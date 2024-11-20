import streamlit as st
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
from streamlit_current_location import current_position
import manage_page

# 各ページのモジュールをインポート
import home, register, ranking, reference, success, fail, confirm, registered, reconfirm
import const

import sqlite3
import hashlib

CONTAINER_HEIGHT = 660

# ページの見た目に関する設定を行う
st.set_page_config(layout="wide")  # ページのレイアウトをワイドに設定
st.markdown(const.HIDE_ST_STYLE, unsafe_allow_html=True)  # スタイルの適用（具体的なスタイルはconstからインポート）

# ページの最大高さを設定するCSSを定義
st.markdown("""
    <style>
    /* モバイルデバイス用のスタイル */
    @media (max-width: 600px) { 
        .block-container {
            overflow-y: auto;   /* 高さを超えたらスクロールを許可 */
            padding-top: 0;
            padding-bottom: 0;
        }
        /* コンテナの高さを自動に設定 */
        .container {
            height: auto;
        }
    }

    /* タブレットデバイス用のスタイル */
    @media (min-width: 601px) and (max-width: 1024px) {
        .container {
            height: 600px; /* タブレットデバイス用のコンテナ高さ */
            padding: 30px; /* パディングを追加 */
        }
    }

    /* デスクトップ用のスタイル */
    @media (min-width: 1025px) {
        .container {
            height: 700px; /* デスクトップ用のコンテナ高さ */
            padding: 40px; /* パディングを追加 */
        }
    }
    </style>
    """, unsafe_allow_html=True)


    

# パスワードをハッシュ化する関数
def hash_password(password: str) -> str:
    # パスワードをバイト型にエンコード
    password_bytes = password.encode()
    
    # SHA-256ハッシュオブジェクトを作成
    sha256_hash = hashlib.sha256()
    
    # パスワードをハッシュオブジェクトに追加
    sha256_hash.update(password_bytes)
    
    # ハッシュ値を16進数文字列として取得
    hashed_password = sha256_hash.hexdigest()
    
    print(hashed_password)  # デバッグ用にハッシュ値を表示
    
    return hashed_password

# セッションステートにページがなければ初期化
if 'page' not in st.session_state:
    st.session_state["page"] = "home"  # デフォルトページを"home"に設定

# 認証状態がセッションステートにない場合、初期化
if 'authentication_status' not in st.session_state:
    st.session_state["authentication_status"] = False

if 'ref_flag' not in st.session_state:
    st.session_state["ref_flag"] = "home"
    
if 'date' not in st.session_state:
    st.session_state["date"] = ""
    
if 'time' not in st.session_state:
    st.session_state["time"] = ""

if 'success_flag' not in st.session_state:
    st.session_state["success_flag"] = False

if 'location' not in st.session_state:
    st.session_state["location"] = ""
    
if 'success_message' not in st.session_state:
    st.session_state["success_message"] = False

if 'login_fale_message' not in st.session_state:
    st.session_state["login_fale_message"] = False


position = None
position = current_position()

if position != None:
    if ('current_latitude' not in st.session_state) and ('current_longitude' not in st.session_state):
        st.session_state["current_latitude"] = position['latitude']
        st.session_state["current_longitude"] = position['longitude']
        #print(position['latitude'])


# SQLite3データベースに接続
db_path = "database.db"  # データベースファイルのパス
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# ユーザー情報をデータベースから取得
cursor.execute("SELECT id, username, password, nickname, level FROM users")
user_data = cursor.fetchall()

# 認証用の設定情報を作成
config = {
    'usernames': {
        user[1]: {
            'id': user[0],
            'name': user[3],    # ニックネームを取得
            'password': user[2],  # ハッシュ化されたパスワード
            'level': user[4],    # ユーザーレベル
            'email': ""  # メールは空のまま
        } for user in user_data
    }
}

# 認証オブジェクトを作成（クッキー情報も含む）
authenticator = stauth.Authenticate(
    credentials=config,  # 認証用のユーザー情報を渡す
    cookie_name="pre_diary_session",  # クッキーの名前
    cookie_key="some_random_key",     # クッキーキーを指定
    cookie_expiry_days=1  # クッキーの有効期限を1日に設定
)

# ログイン画面の表示
authenticator.login()

# ログイン状態に基づいて表示を切り替える
if st.session_state["authentication_status"]:
    st.session_state["login_fale_message"] = False
    st.session_state["id"] = config['usernames'][st.session_state["username"]]['id']
    
    # サイドバーにログインユーザー情報を表示
    with st.sidebar:
        st.markdown(f'### ネーム： {st.session_state["name"]}')
        user_level = config['usernames'][st.session_state["username"]]['level']  # ユーザーレベルを取得
        st.markdown(f'### レベル： {user_level}')  # レベルを表示
        authenticator.logout('Logout', 'sidebar')  # ログアウトボタン

    # ページのコンテンツ表示（コンテナを使用）
    with st.container(height = CONTAINER_HEIGHT):  # コンテナの高さを指定
        if st.session_state["page"] == "home":
            home.show_page()
        elif st.session_state["page"] == "reference":
            reference.show_page()
        elif st.session_state["page"] == "success":
            success.show_page()
        elif st.session_state["page"] == "fail":
            fail.show_page()
        elif st.session_state["page"] == "register":
            register.show_page()
        elif st.session_state["page"] == "ranking":
            ranking.show_page()
        elif st.session_state["page"] == "confirm":
            confirm.show_page()
        elif st.session_state["page"] == "registered":
            registered.show_page()
        elif st.session_state["page"] == "reconfirm":
            reconfirm.show_page()

    # ページ切り替え用のメニュー
    with st.container():
        selected3 = option_menu(None, ["ホーム", "登録", "ランク"], 
            icons=['house', 'pencil-square', "graph-up-arrow"],  # アイコンを設定
            menu_icon="cast", default_index=0, orientation="horizontal",  # 水平方向にメニューを配置
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"font-size": "25px", "display": "flex",  "align-items": "center", "justify-content": "center", "padding":"2px" }, 
                "nav-link": {"font-size": "0px", "text-align": "left", "margin":"0px"},  # ナビゲーションリンクのスタイル
                "nav-link-selected": {"background-color": "#C0C0C0"},  # 選択されたリンクのスタイル
            },
            on_change=manage_page.flag_change,  # ページ切り替え用の関数を呼び出す
            key='option'  # キーを指定してセッションステートで管理
        )


# サインアップ用
if st.session_state["authentication_status"] == False:
    # ボックスの中に動的な内容を表示
    with st.form("signup_form", clear_on_submit=False):
        st.subheader("Signup")
        new_user = st.text_input("ユーザー名を入力してください")
        new_password = st.text_input("パスワードを入力してください",type='password')
        new_nick_name = st.text_input("ニックネームを入力してください")
        submitted = st.form_submit_button("Create")

        if submitted:
            try:
                cursor.execute('INSERT INTO users(username,password,nickname,level) VALUES (?,?,?,?)',(new_user, new_password, new_nick_name, 1))
                conn.commit()
                st.success("アカウントの作成に成功しました")
            except:
                st.error("アカウントの作成に失敗しました")

# データベース接続を閉じる
conn.close()
