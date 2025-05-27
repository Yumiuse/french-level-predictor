# french-level-predictor

**フランス語レベル予測器** は、単語や短いフランス語テキストの難易度（CEFRレベル）を推定するシンプルなWebアプリケーションです。Streamlit を使って手軽に動かせるので、学習者や教材作成者の方もすぐに使えます。

---

## 🔍 主な機能

* **単語レベル予測**: 個別のフランス語単語に対して A1〜C2 に相当する難易度を推定
* **未知語フォールバック**: 辞書に登録されていない語は、`predict_level.py` 内の `predict_levels` 関数の else ブロックで定義された頻度ベースのロジック（`avg_freq` が上位 33% 以上なら Level1、上位 66% 以上なら Level2、その他は Level3）により自動でレベルを推定
* **モデル解説**: scikit-learn & XGBoost を用いた学習パイプラインを構築し、`train_model.py` でモデルを学習・保存
* **即時デプロイ**: Streamlit Cloud へのシームレスなデプロイ対応

---

## 🚀 セットアップ & 実行

1. **リポジトリをクローン**

   ```bash
   git clone https://github.com/Yumiuse/french-level-predictor.git
   cd french-level-predictor
   ```

2. **仮想環境の作成 & 有効化**

   ```bash
   python3.12 -m venv venv-fc
   source venv-fc/bin/activate
   ```

3. **依存パッケージのインストール**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **ローカル起動**

   ```bash
   streamlit run flashcard-core/streamlit_app.py
   ```

   ブラウザで `http://localhost:8501` を開いて操作できます。

---

## 📁 ディレクトリ構成

```
french-level-predictor/
├── data/                          # コーパス用CSVファイル (.csv)
├── flashcard-core/                # アプリ本体コード & モデル
│   ├── data/                      # 内部用マスターコーパス
│   ├── label_encoder.pkl          # ラベルエンコーダ
│   ├── level_model.pkl            # 学習済みモデルパイプライン
│   ├── predict_level.py           # 推論ロジック
│   ├── streamlit_app.py           # Streamlit アプリ
│   └── train_model.py             # モデル学習スクリプト
├── requirements.txt               # 必須ライブラリ一覧
└── README.md                      # 本ドキュメント
```

---

## ☁️ デプロイ (Streamlit Cloud)

1. GitHub にプッシュ
2. Streamlit Cloud で新規アプリ作成

   * **リポジトリ**: `Yumiuse/french-level-predictor`
   * **ブランチ**: `main`
   * **Main file path**: `flashcard-core/streamlit_app.py`
   * **Python バージョン**: 3.12
3. 自動ビルド & 公開されます。

---

## 🛠️ 今後の改善案

* モバイル向けUIの最適化
* テキスト（複数単語／文章）対応の強化
* FastAPI 化して REST API として提供
* UI テーマ切り替え、カスタムモデル読み込み対応

---

## 📝 ライセンス

このプロジェクトは **MIT License** の下で公開しています。

---

> **Author**: Yumiuse
> **Created**: May 2025
