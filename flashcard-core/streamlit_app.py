# flashcard-core/streamlit_app.py

import os, sys
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from predict_level import predict_levels

# ページ設定
st.set_page_config(page_title="French Level Predictor")
st.title("フランス語 単語レベル予測器")

# ─── セッションステート初期化 ───────────────────────────────────
if "input_text" not in st.session_state:
    st.session_state["input_text"] = ""

# ─── クリア用コールバック ────────────────────────────────────────
def clear_input():
    st.session_state["input_text"] = ""

# ─── テキスト入力 ───────────────────────────────────────────────
text = st.text_input(
    "フランス語の単語を入力してください",
    key="input_text"
)

# ─── ボタンを横並びに配置 ───────────────────────────────────────
col1, col2 = st.columns([1, 1])
with col1:
    predict_clicked = st.button("レベルを予測")
with col2:
    clear_clicked = st.button("クリア", on_click=clear_input)

# ─── 予測・表示処理 ────────────────────────────────────────────
if predict_clicked:
    word = st.session_state.input_text.strip()
    if not word:
        st.warning("単語を入力してください。")
    else:
        with st.spinner("🔄 判定中…"):
            level = predict_levels([word])[0]
        st.success(f"予測レベル: {level}")
