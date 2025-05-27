# flashcard-core/streamlit_app.py

import os
import sys
# Add the directory of this file to Python path so predict_level can be imported
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from predict_level import predict_levels
import logging
import traceback

# Configure logging to output INFO level messages
logging.basicConfig(level=logging.INFO)

# Streamlit app title
st.title("フランス語レベル予測器")

# Input area for French text
text = st.text_area("フランス語の文章を入力してください")

# Button to trigger prediction
if st.button("判定する"):
    # Indicate processing
    st.write("🔄 判定中…")
    logging.info(f"▶️ 入力テキスト: {text!r}")
    try:
        # Call the prediction function
        result = predict_levels(text)
        logging.info(f"✅ 予測結果: {result!r}")
        # Display success message with the predicted level
        st.success(f"予測レベル: **{result}**")
    except Exception as e:
        # If an error occurs, display it on the Streamlit UI
        st.error("❗️ 予測中にエラーが発生しました。以下をご確認ください。")
        st.error(e)
        # Show full traceback for debugging
        st.text(traceback.format_exc())
