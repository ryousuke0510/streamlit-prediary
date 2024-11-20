HIDE_ST_STYLE = """
                <style>
                div[data-testid="stToolbar"] {
                    display: none; /* ツールバーを完全に非表示に */
                }
                div[data-testid="stDecoration"] {
                    display: none; /* 装飾を完全に非表示に */
                }
                #MainMenu {
                    display: none; /* メインメニューを完全に非表示に */
                }
                header {
                    display: none; /* ヘッダーを完全に非表示に */
                }
                footer {
                    display: none; /* フッターを完全に非表示に */
                }
                .appview-container .main .block-container {
                    padding-top: 1rem;
                    padding-right: 3rem;
                    padding-left: 3rem;
                    padding-bottom: 1rem;
                }  
                .reportview-container {
                    padding-top: 0rem;
                    padding-right: 3rem;
                    padding-left: 3rem;
                    padding-bottom: 0rem;
                }
                header[data-testid="stHeader"] {
                    z-index: -1; /* z-indexの調整（必要なければ削除可） */
                }
                div[data-testid="stToolbar"] {
                    z-index: 100; /* ツールバーのz-index */
                }
                div[data-testid="stDecoration"] {
                    z-index: 100; /* 装飾のz-index */
                }
                </style>
"""
