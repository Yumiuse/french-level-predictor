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

import sys
import joblib
import pandas as pd

# Paths to the saved model and encoder
MODEL_PATH = 'level_model.pkl'
ENCODER_PATH = 'label_encoder.pkl'

# Load full corpus for feature lookup
try:
    df_master = pd.read_csv('data/mettre_fin_Lexique_translated_v6w_修正済み.csv')
except FileNotFoundError:
    sys.exit("Error: Master data file not found at 'data/mettre_fin_Lexique_translated_v6w_修正済み.csv'.")


def load_pipeline(model_path=MODEL_PATH):
    """
    Load the trained pipeline from disk.
    """
    try:
        pipeline = joblib.load(model_path)
    except FileNotFoundError:
        sys.exit(f"Error: Model file not found at '{model_path}'.")
    return pipeline


def load_label_encoder(encoder_path=ENCODER_PATH):
    """
    Load the label encoder that maps label codes to original levels.
    """
    try:
        le = joblib.load(encoder_path)
    except FileNotFoundError:
        sys.exit(f"Error: Encoder file not found at '{encoder_path}'.")
    return le


def prepare_input(words):
    """
    Prepare a DataFrame matching training features:
      - 'lemme': word lemma or raw input
      - 'cgram', 'genre', 'avg_freq' looked up from master corpus or fallback defaults
    """
    rows = []
    for w in words:
        w_str = w.strip()
        match = df_master[df_master['lemme'] == w_str]
        if not match.empty:
            row = match.iloc[0]
            avg = ((row.get('freqlemfilms2', 0) + row.get('freqlemlivres', 0)) / 2) or 0.0
            rows.append({
                'lemme': row['lemme'],
                'cgram': row['cgram'],
                'genre': row.get('genre', 'none') or 'none',
                'avg_freq': avg
            })
        else:
            # Unknown word: fallback to average frequency of corpus
            avg_global = df_master['freqlemfilms2'].mean() if 'freqlemfilms2' in df_master else 0.0
            rows.append({
                'lemme': w_str,
                'cgram': 'unknown',
                'genre': 'none',
                'avg_freq': avg_global
            })
    return pd.DataFrame(rows)


def predict_levels(words):
    """
    Given a list of words, return their predicted levels.
    """
    pipeline = load_pipeline()
    le = load_label_encoder()
    df_input = prepare_input(words)
    codes = pipeline.predict(df_input)
    levels = le.inverse_transform(codes)
    return levels


def print_usage():
    print("Usage: python predict_level.py <word1> <word2> ...")


if __name__ == '__main__':
    input_words = sys.argv[1:]
    if not input_words:
        print_usage()
        sys.exit(1)

    preds = predict_levels(input_words)
    for word, level in zip(input_words, preds):
        print(f"{word} -> Level {level}")
