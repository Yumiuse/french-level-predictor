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
#   - Prepares input DataFrame with required features
#   - Predicts numeric codes and maps back to original level labels
#   - Prints results in the format: word -> Level X
# 
# Notes:
#   - Ensure level_model.pkl and label_encoder.pkl are in the same directory.
#   - Update MODEL_PATH and ENCODER_PATH constants if files are located elsewhere.
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


rows = []
    for w in words:
        match = df_master[df_master['lemme'] == w]
        if not match.empty:
            row = match.iloc[0]
            avg = ((row.get('freqlemfilms2',0) + row.get('freqlemlivres',0)) / 2) or 0.0
            rows.append({
                'lemme': row['lemme'],
                'cgram': row['cgram'],
                'genre': row.get('genre','none') or 'none',
                'avg_freq': avg
            })
        else:
            rows.append({
                'lemme': w,
                'cgram': 'unknown',
                'genre': 'none',
                'avg_freq': df_master['freqlemfilms2'].mean()
            })
    return pd.DataFrame(rows)

def predict_levels(words):
    """
    Given a list of words, return their predicted levels.
    """
    pipeline = load_pipeline()
    le = load_label_encoder()
    df_input = prepare_input(words)
    # Predict numeric codes
    codes = pipeline.predict(df_input)
    # Map back to original level labels
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
