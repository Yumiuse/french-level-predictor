# french-level-predictor

CEFRレベル予測モデル

このリポジトリはフランス語単語の難易度（レベル）を判定する機械学習モデルの学習から推論、StreamlitによるインタラクティブUIまでを提供します。フラッシュカード式アプリの実装は別リポジトリ（`french-flashcard-app`）で管理するため、本リポジトリはあくまでレベル判定機能に特化しています。

## 目次

1. [概要](#概要)
2. [前提条件](#前提条件)
3. [データ準備](#データ準備)
4. [モデル訓練](#モデル訓練)
5. [モデル出力ファイル](#モデル出力ファイル)
6. [推論スクリプト](#推論スクリプト)
7. [Streamlitアプリ](#streamlitアプリ)
8. [リポジトリ構成](#リポジトリ構成)
9. [今後の展望](#今後の展望)

---

## 概要

* `train_model.ipynb`: データ前処理、XGBoostモデル訓練、評価、5-fold CVを行うJupyter Notebook
* `predict_level.py`: コマンドラインから単語を入力し、レベルを判定して出力するスクリプト
* `streamlit_app.py`: ブラウザ上で単語を入力し、「レベルを予測」ボタンで判定結果を表示するStreamlitアプリ
* `data/`: 単語データ（CSV）
* `requirements.txt`: 必要パッケージ一覧
* `level_model.pkl`, `label_encoder.pkl`: 学習済みモデル＆エンコーダ

## 前提条件

* Python 3.8以上
* GitおよびGitHubアカウント
* 必要パッケージをインストール

  ```bash
  pip install -r requirements.txt
  python -m spacy download fr_core_news_sm
  ```

## データ準備

1. `data/mettre_fin_Lexique_translated_v6w_修正済み.csv` を `data/` フォルダに配置
2. 必要に応じてデータをクリーニング・更新

## モデル訓練

1. Colabまたはローカル環境で `train_model.ipynb` を開く
2. Notebook内の最終セルに以下を追加・実行してモデルファイルを生成

   ```python
   import joblib
   joblib.dump(pipeline, 'level_model.pkl')
   joblib.dump(le,       'label_encoder.pkl')
   ```
3. `level_model.pkl` と `label_encoder.pkl` が出力されます

## モデル出力ファイル

* `level_model.pkl`: 訓練済みパイプライン（前処理＋XGBoost）
* `label_encoder.pkl`: ラベルエンコーダ（レベルの逆変換用）

## 推論スクリプト

以下のコマンドで単語のレベルを判定できます

```bash
python predict_level.py bonjour salut inconnu
```

出力例:

```
bonjour -> Level 1
salut   -> Level 1
inconnu -> Level 2
```

## Streamlitアプリ

ブラウザでインタラクティブにレベル予測を行います

```bash
streamlit run streamlit_app.py
```

* 入力欄にフランス語単語を入力
* 「レベルを予測」ボタンを押下
* 予測レベルが表示されます

## リポジトリ構成

```
/
├─ data/
│  └─ mettre_fin_Lexique_translated_v6w_修正済み.csv
├─ train_model.ipynb
├─ predict_level.py
├─ streamlit_app.py
├─ level_model.pkl
├─ label_encoder.pkl
└─ requirements.txt
```

## 今後の展望

* 別コーパスによる汎化性能検証
* 他アルゴリズム・ハイパーパラメータチューニング
* FastAPIなどでAPI化
* モバイルアプリやフラッシュカードアプリへの統合＼
