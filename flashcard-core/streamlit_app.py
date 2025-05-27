# streamlit_app.py

# 必要な部品（Streamlitなど）を使えるように準備します
import streamlit as st
# predict_level.py ファイルから、レベルを予測する機能 (predict_levels) を借りてきます
# from predict_level import predict_levels # ← ChatGPTが sys.path をいじったので、これは元のままで良いかもしれません
# もしエラーが出るようなら、ChatGPTが提案した以下の2行と、上の行を入れ替えます
import os, sys
sys.path.insert(0, os.path.dirname(__file__)) # これで同じフォルダ内のファイルを見つけやすくするおまじない
from predict_level import predict_levels

# --- アプリが「入力された文字」を覚えておくための「一時的な記憶場所」の準備 ---
# もし、まだ "input_text" という名前の記憶場所がなければ、
# 新しく作って、最初は空っぽ（""）にしておきます。
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# --- 画面のタイトルなどを表示 ---
st.title("フランス語レベル予測器")

# --- 文字を入力する箱を表示 ---
# 「フランス語の文章を入力してください」という案内付きの、複数行入力できる箱です。
# この箱に表示される文字は、「一時的な記憶場所 ("input_text")」に入っている文字です。
# そして、ユーザーがこの箱に何か入力すると、それが text_input_value という名前の入れ物に入ります。
text_input_value = st.text_area(
    "フランス語の文章を入力してください",
    value=st.session_state.input_text,  # 「一時的な記憶場所」の文字を表示する
    key="user_input_area" # この入力箱自体の名前（なんでも良いですが、記憶場所とは違う名前にします）
)

# --- 「レベルを予測」ボタンと「クリア」ボタンを横に並べるための準備 ---
col1, col2 = st.columns(2) # 画面を左右2つの列に分けます

# --- 左側の列 (col1) に「レベルを予測」ボタンを置く ---
with col1:
    if st.button("レベルを予測"): # もし「レベルを予測」ボタンが押されたら…
        if not text_input_value.strip(): # 入力箱が空っぽ、またはスペースだけだったら…
            st.warning("文章を入力してください。") # 注意メッセージを出す
        else: # 何か文字が入力されていたら…
            st.write("🔄 判定中…") # 「判定中…」と表示
            try:
                # 「predict_levels」機能を使ってレベルを予測します。
                # 入力箱の文字 (text_input_value) を渡します。
                # (predict_levels がリストを期待するなら [text_input_value.strip()] のように調整)
                result = predict_levels([text_input_value.strip()]) # predict_levels がリストを想定しているのでリストで渡す
                st.success(f"予測レベル: **{result}**") # 結果を表示
            except Exception as e: # もし予測中に何かエラーが起きたら…
                st.error("❗️ 予測中にエラーが発生しました。") # エラーメッセージを表示
                st.error(e) # エラーの詳細も表示
                # import traceback # traceback を使うなら、ファイルの先頭で import が必要
                # st.text(traceback.format_exc()) # もっと詳しいエラー情報（開発者向け）

# --- 右側の列 (col2) に「クリア」ボタンを置く ---
with col2:
    if st.button("クリア"): # もし「クリア」ボタンが押されたら…
        # 「一時的な記憶場所 ("input_text")」の中身を空っぽにします。
        st.session_state.input_text = ""
        # Streamlit に「画面の部品を作り直してね」とお願いして、
        # 表示を最新の状態に更新します。
        st.rerun()