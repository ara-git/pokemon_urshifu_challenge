"""
ロジスティック回帰で学習する
"""

from sklearn.model_selection import StratifiedKFold
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

def train_logistic(train_x, train_y, test_x, test_y):
    # クロスバリデーションの設定
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
    
    score_list = []
    for fold_id, (train_index, valid_index) in enumerate(cv.split(train_x, train_y)):
        # 学習データと検証データに分割する
        train_cv_x = train_x.iloc[train_index, : ]
        valid_x = train_x.iloc[valid_index, : ]
        train_cv_y = train_y.iloc[train_index]
        valid_y = train_y.iloc[valid_index]

        model = LogisticRegression(verbose=0)

        # 学習
        model.fit(train_cv_x, train_cv_y)

        # 検証
        pred_y = model.predict(test_x)
        score = accuracy_score(test_y, pred_y)
        score_list.append(score)

    # 平均スコアを計算する
    score_list = np.array(score_list)
    average_score = np.average(score_list)
    print("logistic_score:", average_score)

    return pd.DataFrame([average_score], columns = ["score"])