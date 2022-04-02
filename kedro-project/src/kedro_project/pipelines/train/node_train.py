#学習
from sklearn.ensemble import GradientBoostingClassifier
import numpy as np
import pandas as pd

"""
def train_GBDT(train_x, train_y,test_x, test_y):
    clf = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1,
            max_depth=1).fit(train_x, train_y)

    print ("Predict ",clf.predict(test_x))
    print ("Expected", test_y)
    print (clf.score(test_x, test_y))

    return pd.DataFrame([1,2])
"""
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