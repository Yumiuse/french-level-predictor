french-level-predictor
フランス語レベル予測器は、単語（または短い語句）の難易度を Level 1〜3 で推定するシンプルなアプリです。UI は Streamlit、推論は scikit-learn & XGBoost を使用します。

🔍 主な機能
単語レベル予測：predict_level.py で 1語ずつ推定（出力例: bonjour -> Level 1）

未知語フォールバック：マスターコーパスに無い語は頻度ベースで Level を推定
（avg_freq が上位33%以上→Level2、上位66%以上→Level1、それ以外→Level3）

モデル学習：train_model.py / train_model.ipynb で学習・保存（level_model.pkl, label_encoder.pkl）

即時実行：ローカルでも Streamlit Cloud でもすぐ動作

※ CEFR（A1〜C2）と厳密に対応させる場合は、Level 1–3 の対応表を README に追記してください。

 セットアップ & 実行
クローン

bash
コピーする
編集する
git clone https://github.com/Yumiuse/french-level-predictor.git
cd french-level-predictor
Python バージョン（pyenv 利用時のみ）
.python-version は 3.13.3 を指定しています。

bash
コピーする
編集する
pyenv local 3.13.3   # 任意
仮想環境の作成 & 有効化

bash
コピーする
編集する
python -m venv .venv
source .venv/bin/activate
依存インストール

bash
コピーする
編集する
pip install -r requirements.txt
コマンドライン推論（例）

bash
コピーする
編集する
python flashcard-core/predict_level.py bonjour merci
Streamlit アプリ

bash
コピーする
編集する
streamlit run flashcard-core/streamlit_app.py
ブラウザで http://localhost:8501 を開きます。

 ディレクトリ構成
bash
コピーする
編集する
french-level-predictor/
├── .python-version            # 3.13.3（pyenv を使う場合）
├── README.md
├── requirements.txt
├── docs/
│   └── development_notes.md
└── flashcard-core/
    ├── data/
    │   └── mettre_fin_Lexique_translated_v6w_修正済み.csv
    ├── label_encoder.pkl
    ├── level_model.pkl
    ├── predict_level.py
    ├── streamlit_app.py
    ├── train_model.ipynb      # （任意で training/ に移動可）
    └── train_model.py         # （任意で training/ に移動可）
☁️ デプロイ（Streamlit Cloud）
Repository: Yumiuse/french-level-predictor

Branch: main

Main file path: flashcard-core/streamlit_app.py

Python: 3.13（.python-version に追従）

公開URL（運用中）：
https://french-level-predictor-wycydbupdigjyjajobkzys.streamlit.app/

 今後の改善
モバイルUI最適化 / テーマ切替

複数語・文章入力の精度改善

FastAPI 化（REST API 提供）

学習側で save_model()（.json）保存への切替

 ライセンス
MIT License

Author: Yumiuse（May 2025）