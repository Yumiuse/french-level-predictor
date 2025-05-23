import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import joblib

def main():
    # --- 1) データ読み込み ---
    df = pd.read_csv('data/mettre_fin_Lexique_translated_v6w_修正済み.csv')
    df['lemme'] = df['lemme'].fillna('')
    df['cgram'] = df['cgram'].fillna('unknown').astype(str)
    df['genre'] = df['genre'].fillna('none').astype(str)

    le = LabelEncoder()
    df['level_code'] = le.fit_transform(df['level'])

    df['avg_freq'] = ((df['freqlemfilms2'] + df['freqlemlivres']) / 2).fillna(0)
    X = df[['lemme', 'cgram', 'genre', 'avg_freq']]
    y = df['level_code']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    preprocessor = ColumnTransformer([
        ('tfidf', TfidfVectorizer(max_features=2000), 'lemme'),
        ('ohe',   OneHotEncoder(handle_unknown='ignore', sparse_output=False), ['cgram','genre']),
        ('num',   StandardScaler(), ['avg_freq']),
    ], remainder='drop')

    pipeline = Pipeline([
        ('pre', preprocessor),
        ('clf', XGBClassifier(
            max_depth=4,
            n_estimators=200,
            objective='multi:softprob',
            eval_metric='mlogloss',
            use_label_encoder=False,
            random_state=42,
            n_jobs=-1
        ))
    ])

    print("▶ Training XGBoost model...")
    pipeline.fit(X_train, y_train)

    print("▶ Evaluating on test set...")
    y_pred = pipeline.predict(X_test)
    target_names = [f"Level {c}" for c in le.classes_]
    print(classification_report(y_test, y_pred, target_names=target_names, digits=3))

    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(cm, display_labels=target_names)
    disp.plot()
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.show()

    print("▶ Running Stratified K-Fold CV ...")
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scoring = ['accuracy','precision_macro','recall_macro','f1_macro']
    cv_results = cross_validate(
        pipeline,
        X,
        y,
        cv=skf,
        scoring=scoring,
        n_jobs=-1,
        return_train_score=False
    )
    for metric in scoring:
        scores = cv_results[f'test_{metric}']
        print(f"{metric}: {scores.mean():.3f} ± {scores.std():.3f}")

    # モデル保存
    joblib.dump(pipeline, 'level_model.pkl')
    joblib.dump(le,       'label_encoder.pkl')
    print("level_model.pkl と label_encoder.pkl を保存しました")

if __name__ == '__main__':
    main()
