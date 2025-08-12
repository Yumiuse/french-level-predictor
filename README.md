コピペ用の完全版READMEです：

```md
# french-level-predictor

**フランス語レベル予測器**は、単語（または短い語句）の難易度を **Level 1〜3** で推定するシンプルなアプリです。UI は **Streamlit**、推論は **scikit-learn & XGBoost** を使用します。

---

## 🔍 主な機能
- **単語レベル予測**：`predict_level.py` で 1語ずつ推定（例: `bonjour -> Level 1`）
- **未知語フォールバック**：コーパスに無い語は頻度ベースで推定  
  - `avg_freq` が上位 **66% 以上 → Level 1** / 上位 **33% 以上 → Level 2** / それ以外 → **Level 3**
- **モデル学習**：`train_model.py` / `train_model.ipynb` で学習・保存（`level_model.pkl`, `label_encoder.pkl`）
- **即時実行**：ローカルでも Streamlit Cloud でもすぐ動作

> ※ CEFR（A1〜C2）と厳密対応させる場合は、`Level 1–3` の対応表を別途定義してください。

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

