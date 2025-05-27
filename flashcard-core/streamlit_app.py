import os, sys
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from predict_level import predict_levels

st.set_page_config(page_title="French Level Predictor")
st.title("フランス語 単語レベル予測器")

# 1) テキスト入力にキーをつける
text = st.text_input("フランス語の単語を入力してください", key="input_text")

# 2) 「クリア」ボタンを追加してセッションステートをリセット
if st.button("クリア"):
    st.session_state.input_text = ""  # テキストボックスを空に

# 3) 判定ボタンを押したらスピナーを回しつつ予測
if st.button("レベルを予測"):
    if not text.strip():
        st.warning("単語を入力してください。")
    else:
        # with スピナー context で「判定中…」を表示
        with st.spinner("🔄 判定中…"):
            level = predict_levels([text.strip()])[0]
        # 結果を表示
        st.success(f"予測レベル: {level}")
