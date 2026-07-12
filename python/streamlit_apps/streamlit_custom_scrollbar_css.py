import streamlit as st

# スクロールバーのデザインを適用するCSS
scrollbar_css = """
    <style>
    /* Webkitベースのブラウザ（Chrome, Edge, Safari）用 */
    ::-webkit-scrollbar {
        width: 12px; /* スクロールバーの幅を指定 */
    }

    ::-webkit-scrollbar-thumb {
        background: #888; /* スクロールバーの色 */
        border-radius: 6px; /* 角を丸くする */
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #555; /* ホバー時の色 */
    }

    /* Firefox用（CSSプロパティを適用できるバージョンのみ） */
    html {
        scrollbar-width: thin; /* "auto" / "thin" / "none" */
        scrollbar-color: #888 #f1f1f1; /* スクロールバーと背景の色 */
    }
    </style>
"""

# Streamlitアプリの設定
st.set_page_config(page_title="Scrollbar Customization", layout="wide")

# CSSを適用
st.markdown(scrollbar_css, unsafe_allow_html=True)

st.title("カスタムスクロールバーのテスト")

# 長いテキストを追加してスクロールバーを表示
st.write("### スクロールしてみてください")
st.write("このボックスが長いので、スクロールバーが表示されます。" * 50)