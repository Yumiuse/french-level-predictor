import streamlit as st
import spacy
from predict_level import predict_levels

# spaCy モデルロード（起動時1回）
nlp = spacy.load("fr_core_news_sm")

st.set_page_config(page_title="French Level Predictor")
st.title("フランス語 単語レベル予測器")

word = st.text_input("フランス語の単語を入力してください")
if st.button("レベルを予測"):
    if not word.strip():
        st.warning("単語を入力してください。")
    else:
        # 生の入力を lemma に変換
        doc = nlp(word.strip())
        lemma = doc[0].lemma_ if doc else word.strip()
        # predict_levels はリスト受けなので [lemma]
        level = predict_levels([lemma])[0]
        st.success(f"入力: {word} → 原形: {lemma} → 予測レベル: {level}")
