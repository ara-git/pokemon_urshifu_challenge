#学習
import xgboost as xgb
from sklearn.model_selection import cross_validate,cross_val_predict, StratifiedKFold
import pandas as pd
import numpy as np
import sklearn
import matplotlib.pyplot as plt
import japanize_matplotlib

def train_GBDT(train_x, train_y,test_x, test_y):
    # ハイパーパラメータを指定して学習実行
    train_params = {
        'objective': 'binary:logistic',
        'eval_metric': 'logloss',
        'learning_rate': 0.01,
        'max_depth': 4,
        'n_estimators': 60,
        'colsample_bytree': 0.6
    }
    clf = xgb.XGBClassifier(**train_params)

    clf.fit(train_x, train_y, eval_set=[[test_x, test_y]])

    model = xgb.XGBClassifier(n_estimators=20, random_state=71)
    model.fit(train_x, train_y)
    
    # 出力(1): 検証用データに対する精度を確認
    booster = clf.get_booster()
    dtest = xgb.DMatrix(test_x, label=test_y)
    y_test_pred_prob = booster.predict(dtest)
    y_test_pred = np.where(y_test_pred_prob > 0.5, 1, 0)
    acc = sklearn.metrics.accuracy_score(test_y, y_test_pred)

    print("FFF")
    print(acc)
    
    # 出力(2): 特徴量の重要度を描画
    _, ax = plt.subplots(figsize=(12, 12))
    xgb.plot_importance(booster,
                        ax=ax,
                        importance_type='gain',
                        show_values=False)

    plt.show()
    return pd.DataFrame([1,2])
    """
    # 説明変数・被説明変数を定義
    y = df["target"]
    X = df[df.columns[df.columns != 'target']]

    # 学習し、closs-varidation
    splits = 5
    skf = StratifiedKFold(n_splits=splits, shuffle=True, random_state=42)
    score_funcs = ["accuracy","precision_macro","recall_macro","f1_macro"]
    
    clf = xgb.XGBClassifier(objective="binary:logistic")
    
    score = cross_validate(clf, X, y, cv=skf, scoring=score_funcs,return_estimator=True)
    
    print(score["test_accuracy"].mean())
    print(score["test_precision_macro"].mean())
    print(score["test_recall_macro"].mean())
    print(score["test_f1_macro"].mean())
    return pd.DataFrame([1,2])
    """
