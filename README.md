コピペ用の完全版READMEです：

```md
# french-level-predictor

**フランス語レベル予測器**は、単語（または短い語句）の難易度を **Level 1〜3** で推定するシンプルなアプリです。UI は **Streamlit**、推論は **scikit-learn & XGBoost** を使用します。

---

## 🔍 主な機能
- **単語レベル予測**：フランス語単語の難易度を Level 1〜3 で判定
- **コマンドライン実行**：`predict_level.py` でサクッと確認
- **Webアプリ**：Streamlit でブラウザから簡単操作
- **モデル学習**：独自データで再学習可能



---

## 🚀 セットアップ & 実行

### 0) 前提
- Python **3.13.3**（`.python-version` で指定）  
  pyenv を使う場合:
```bash
pyenv local 3.13.3
```

### 1) クローン
```bash
git clone https://github.com/Yumiuse/french-level-predictor.git
cd french-level-predictor
```

### 2) 仮想環境
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3) 依存インストール
```bash
pip install -r requirements.txt
```

### 4) コマンドライン推論（例）
```bash
python flashcard-core/predict_level.py bonjour merci
```

### 5) Streamlit アプリ
```bash
streamlit run flashcard-core/streamlit_app.py
```

→ ブラウザで `http://localhost:8501` を開く

---

## 📁 ディレクトリ構成

```text
french-level-predictor/
├── .python-version            # 3.13.3
├── .gitignore
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
    ├── train_model.ipynb
    └── train_model.py
```

---

## ☁️ デプロイ（Streamlit Cloud）
* **Repository**: `Yumiuse/french-level-predictor`
* **Branch**: `main`
* **Main file path**: `flashcard-core/streamlit_app.py`
* **Python**: `3.13`（`.python-version` に追従）

公開URL： https://french-level-predictor-wycydbupdigjyjajobkzys.streamlit.app/

---

## 🛠 改善予定
* モバイルUI最適化 / テーマ切替
* 複数語・文章入力の精度改善
* FastAPI による REST API 提供
* 学習側で `save_model()`（.json）保存に切替

---

## 📝 ライセンス
MIT License（c）Yumiuse
```

この内容を**全選択(⌘A)→削除→コピペ→保存(⌘S)**してください！
