import logging
import streamlit as st

# グローバルロガー設定関数
@st.cache_resource
def setup_global_logger():
    # ルートロガーの設定
    root_logger = logging.getLogger()
    if not root_logger.handlers:
        # 共通のハンドラーを設定
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)
        root_logger.setLevel(logging.INFO)  # 必要に応じてDEBUGやWARNINGに変更
    return root_logger

# ロガー設定の適用
setup_global_logger()

# Streamlitのログを抑制（必要なら）
logging.getLogger("streamlit").setLevel(logging.WARNING)

# 必要に応じて特定のモジュールをデバッグログにする
logging.getLogger("tool1_logger").setLevel(logging.DEBUG)
logging.getLogger("tool2_logger").setLevel(logging.DEBUG)

# 各ツールからのログ出力例
logging.getLogger("tool1_logger").info("Tool 1 is running.")
logging.getLogger("tool2_logger").info("Tool 2 is running.")