import os, sys
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from predict_level import predict_levels

st.set_page_config(page_title="French Level Predictor")
st.title("フランス語 単語レベル予測器")

# ─── クリア用コールバック ─────────────────────────────────────
def clear_input():
    st.session_state["input_text"] = ""

# ─── テキスト入力 ───────────────────────────────────────────
# key="input_text" を指定
text = st.text_input("フランス語の単語を入力してください", key="input_text")

# ─── クリアボタン ───────────────────────────────────────────
# on_click で clear_input を呼び出す
st.button("クリア", on_click=clear_input)

# ─── 予測ボタン ────────────────────────────────────────────
if st.button("レベルを予測"):
    # 空入力チェック
    if not st.session_state.input_text.strip():
        st.warning("単語を入力してください。")
    else:
        # スピナーを回しながら予測
        with st.spinner("🔄 判定中…"):
            level = predict_levels([st.session_state.input_text.strip()])[0]
        # 結果を表示
        st.success(f"予測レベル: {level}")
