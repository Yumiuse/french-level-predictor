# french-flashcard-portfolio
French Flashcard App with ML level prediction

リポジトリ作成からデータ配置、モデル学習、アプリ連携まで一連の流れ

---

## French-Flashcard-Portfolio プロジェクト作成から現在までの手順メモ

### 1. GitHub リポジトリ作成

1. GitHub 上で `french-flashcard-portfolio` リポジトリを新規作成
2. プライベート／パブリックは用途に合わせて設定
3. 「Initialize this repository with a README」はお好みで

### 2. ローカルにクローン

```bash
git clone git@github.com:<ユーザー名>/french-flashcard-portfolio.git
cd french-flashcard-portfolio
```

### 3. データフォルダの準備

```bash
mkdir -p data
```

### 4. CSV ファイルをコピー＆コミット

```bash
# CSV がある場所（例）からリポジトリ直下の data/ にコピー
cp "/Volumes/SP PC60/ChatGPT_API/input/mettre_fin_Lexique_translated_v6w_修正済み.csv" data/

# Git に登録・コミット・プッシュ
git add data/mettre_fin_Lexique_translated_v6w_修正済み.csv
git commit -m "Add cleaned vocabulary CSV to data/"
git push origin main
```

### 5. モデル訓練スクリプト作成（train\_model.py）

* **目的**：`data/…csv` を読み込んで XGBoost でレベル分類モデル訓練
* **主な内容**：

  1. pandas で CSV 読み込み
  2. LabelEncoder でレベルを数値化
  3. train\_test\_split（stratify）
  4. TF-IDF／OneHot 前処理
  5. XGBClassifier で学習
  6. classification\_report で評価
  7. `level_model.pkl`, `label_encoder.pkl` を出力

> ※詳しいコードは別途 `train_model.py` に記載

### 6. モデル訓練の実行

```bash
python train_model.py
# → 評価結果（accuracy, f1 など）が出力され、
#    level_model.pkl と label_encoder.pkl が生成される
```

### 7. Streamlit アプリ作成（main.py）

* **目的**：ユーザー入力ワードを受け取り、モデルでレベル判定し表示
* **機能**：

  1. `level_model.pkl`, `label_encoder.pkl` の読み込み
  2. 辞書チェック（フランス語文字か／CSV にあるか）
  3. 存在しなければエラー、存在すれば `model.predict()`
  4. 結果を `st.success()` で表示

> ※詳しいコードは別途 `main.py` に記載

### 8. アプリ動作確認

```bash
streamlit run main.py
```

* `/` に `French Word Level Checker` が表示
* 正しい単語 → レベル表示
* 不正な入力 → エラーメッセージ

### 9. README.md にまとめ

* プロジェクト概要・目的
* データ準備手順（data/ 配置方法）
* モデル訓練方法（train\_model.py 実行方法）
* アプリ起動方法（streamlit run main.py）
* 今後の展望（FastAPI 連携、他アルゴリズム比較など）

---

これで「ゼロからデータ配置→モデル学習→アプリ実装→ドキュメント作成」までの全体像が整理できました。
必要に応じて細かい設定や追加タスクを README に書き加えてください。
