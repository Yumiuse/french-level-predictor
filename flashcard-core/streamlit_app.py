# ─── flashcard-core/streamlit_app.py ───────────────────────────────
import os, sys
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from predict_level import predict_levels

# ─── ページ設定 ────────────────────────────────────────────────────
st.set_page_config(page_title="French Level Predictor")
st.title("フランス語 単語レベル予測器")

# ─── モデル読み込みをキャッシュ化 ───────────────────────────────────
@st.cache_resource(show_spinner=False)
def get_predict_fn():
    # predict_levels の中で joblib.load しているならそれを一度だけ実行させる
    return predict_levels

# ─── セッションステート初期化 ─────────────────────────────────────
if "input_text" not in st.session_state:
    st.session_state["input_text"] = ""

def clear_input():
    st.session_state["input_text"] = ""

# ─── 入力 UI ───────────────────────────────────────────────────────
text = st.text_input(
    "フランス語の単語を入力してください",
    key="input_text"
)

col1, col2 = st.columns([1, 1])
with col1:
    predict_clicked = st.button("レベルを予測")
with col2:
    clear_clicked = st.button("クリア", on_click=clear_input)

# ─── 予測・表示 ───────────────────────────────────────────────────
if predict_clicked:
    word = st.session_state.input_text.strip()
    if not word:
        st.warning("単語を入力してください。")
    else:
        # ① キャッシュ化した関数を呼び出してモデルを一度だけロード
        with st.spinner("🔄 モデル読み込み中…"):
            predict_fn = get_predict_fn()

        # ② 予測実行
        with st.spinner("🔄 判定中…"):
            level = predict_fn([word])[0]

        st.success(f"予測レベル: {level}")
# ────────────────────────────────────────────────────────────────────
