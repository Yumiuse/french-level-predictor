
import streamlit as st
from predict_level import predict_levels

st.set_page_config(page_title="French Level Predictor")
st.title("フランス語 単語レベル予測器")

# ユーザー入力
word = st.text_input("フランス語の単語を入力してください")
if st.button("レベルを予測"):
    if not word.strip():
        st.warning("単語を入力してください。")
    else:
        # spaCy を使わず、生入力そのままを予測
        level = predict_levels([word.strip()])[0]
        st.success(f"予測レベル: {level}")
