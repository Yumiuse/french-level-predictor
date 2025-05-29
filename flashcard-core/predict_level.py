# predict_level.py
# ======================================
# Purpose:
#   Provide command-line inference for French flashcard word difficulty levels (CEFR).
#
# Usage:
#   python predict_level.py <word1> <word2> ...
#
# This script:
#   - Loads a trained pipeline (level_model.pkl) and a label encoder (label_encoder.pkl)
#   - Prepares input DataFrame with required features, including handling unknown words
#   - Predicts numeric codes and maps back to original level labels
#   - Prints results in the format: word -> Level X
#
# Notes:
#   - Ensure level_model.pkl and label_encoder.pkl are in the same directory.
#   - CSV data file for master corpus must be at data/mettre_fin_Lexique_translated_v6w_修正済み.csv
#
# Author: Yumiuse
# Created: 2025-05
# ======================================
import os
import sys
import logging
import joblib
import pandas as pd
import numpy as np

# ログ設定
logging.basicConfig(level=logging.INFO)
logging.info("⚙️ predict_level モジュール読み込み完了")

# ベースディレクトリ設定
BASE_DIR = os.path.dirname(__file__)
MODEL_PATH   = os.path.join(BASE_DIR, 'level_model.pkl')
ENCODER_PATH = os.path.join(BASE_DIR, 'label_encoder.pkl')
DATA_PATH    = os.path.join(BASE_DIR, 'data', 'mettre_fin_Lexique_translated_v6w_修正済み.csv')

# マスターコーパスの読み込み
try:
    logging.info(f"🔄 マスターコーパス読み込み: {DATA_PATH}")
    df_master = pd.read_csv(DATA_PATH)
    logging.info("✅ マスターコーパス読み込み完了")
except FileNotFoundError:
    logging.error(f"Error: Master data file not found at '{DATA_PATH}'.")
    sys.exit(f"Error: Master data file not found at '{DATA_PATH}'.")


def load_pipeline(model_path=MODEL_PATH):
    """
    Load the trained pipeline from disk.
    """
    logging.info(f"🔄 モデルロード開始: {model_path}")
    try:
        pipeline = joblib.load(model_path)
        logging.info("✅ モデルロード完了")
    except FileNotFoundError:
        logging.error(f"Error: Model file not found at '{model_path}'.")
        sys.exit(f"Error: Model file not found at '{model_path}'.")
    return pipeline


def load_label_encoder(encoder_path=ENCODER_PATH):
    """
    Load the label encoder that maps label codes to original levels.
    """
    logging.info(f"🔄 ラベルエンコーダロード開始: {encoder_path}")
    try:
        le = joblib.load(encoder_path)
        logging.info("✅ ラベルエンコーダロード完了")
    except FileNotFoundError:
        logging.error(f"Error: Encoder file not found at '{encoder_path}'.")
        sys.exit(f"Error: Encoder file not found at '{encoder_path}'.")
    return le


def prepare_input(words):
    logging.info(f"▶️ prepare_input 呼び出し: {words}")
    rows = []
    for w in words:
        # 小文字化＋正規化＋不可視文字除去
        w_str = w.strip().lower().normalize('NFC').replace('\u200b', '')
        # マッチ有無をデバッグ出力
        exists = (w_str in df_master['lemme'].values)
        print(f"DEBUG: 入力='{w}' → 小文字化='{w_str}' → コーパスに存在? {exists}")
        match = df_master[df_master['lemme'] == w_str]
        if not match.empty:
            row = match.iloc[0]
            avg = ((row.get('freqlemfilms2', 0) + row.get('freqlemlivres', 0)) / 2) or 0.0
            rows.append({
                'lemme': row['lemme'],
                'cgram': str(row['cgram']),
                'genre': str(row.get('genre', 'none')),
                'avg_freq': avg
            })
        else:
            # 未知語は頻度 0 とみなす
            rows.append({
                'lemme': w_str,
                'cgram': 'unknown',
                'genre': 'none',
                'avg_freq': 0.0
            })
    df_input = pd.DataFrame(rows)
    print("DEBUG: prepare_input 後の df_input")
    print(df_input)
    return df_input


def predict_levels(words):
    logging.info(f"▶️ predict_levels 呼び出し: {words}")
    pipeline = load_pipeline()
    le = load_label_encoder()

    freq_series = (
        df_master[['freqlemfilms2','freqlemlivres']]
        .mean(axis=1, skipna=True)
        .fillna(0)
    )
    q1, q2 = np.percentile(freq_series, [33, 66])
    print(f"DEBUG: freq thresholds: q1={q1:.2f}, q2={q2:.2f}")

    results = []
    for w in words:
        df_input = prepare_input([w])
        print("DEBUG: df_input", df_input.to_dict(orient='records'))

        if w.strip().lower() in df_master['lemme'].values:
            # モデルの確率を出力
            probs = pipeline.predict_proba(df_input)[0]
            print(f"DEBUG: モデル predict_proba → {probs}")
            # 予測実行
            code = pipeline.predict(df_input)[0]
            label = le.inverse_transform([code])[0]
            logging.info(f"✅ 予測: {w} -> Level {label}")
            results.append(f"Level {label}")
        else:
            # 未知語フォールバック
            avg_f = df_input.at[0, 'avg_freq']
            if avg_f >= q2:
                lvl = "Level 1"
            elif avg_f >= q1:
                lvl = "Level 2"
            else:
                lvl = "Level 3"
            logging.info(f"🛠 フォールバック結果: {w} -> {lvl}")
            results.append(lvl)

    logging.info(f"🎯 最終結果: {results}")
    return results

def print_usage():
    print("Usage: python predict_level.py <word1> <word2> ...")


if __name__ == '__main__':
    input_words = sys.argv[1:]
    if not input_words:
        print_usage()
        sys.exit(1)

    preds = predict_levels(input_words)
    for word, level in zip(input_words, preds):
        print(f"{word} -> {level}")