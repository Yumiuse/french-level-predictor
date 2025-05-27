# flashcard-core/streamlit_app.py

import os
import sys
# このファイルと同じディレクトリを import パスに追加
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from predict_level import predict_levels
import logging
import traceback

logging.basicConfig(level=logging.INFO)

st.set_page_config(page_title="French Level Predictor")
st.title("フランス語 単語レベル予測器")

word = st.text_input("フランス語の単語を入力してください")
if st.button("レベルを予測"):
    st.write("🔄 判定中…")
    logging.info(f"▶️ 入力単語: {word!r}")
    try:
        level = predict_levels([word.strip()])[0]
        logging.info(f"✅ 予測結果: {level!r}")
        st.success(f"予測レベル: **{level}**")
    except Exception as e:
        st.error("❗️ 予測中にエラーが発生しました。以下をご確認ください。")
        st.error(e)
        st.text(traceback.format_exc())
