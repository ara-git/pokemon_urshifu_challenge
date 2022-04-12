from sklearn.model_selection import StratifiedKFold
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

def train_logistic(df):
    """
    ロジスティック回帰で学習する
    """
    # 説明変数・被説明変数を定義
    y = df["target"]
    x = df[df.columns[df.columns != 'target']]

    # クロスバリデーションの設定
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
    
    score_list = []
    for fold_id, (train_index, test_index) in enumerate(cv.split(x, y)):
        # 学習データと検証データに分割する
        train_x = x.iloc[train_index, : ]
        test_x = x.iloc[test_index, : ]
        train_y = y.iloc[train_index]
        test_y = y.iloc[test_index]
        
        model = LogisticRegression()

        # 学習
        model.fit(train_x, train_y)

        # 検証
        pred_y = model.predict(test_x)
        score = accuracy_score(test_y, pred_y)
        score_list.append(score)

    # 平均スコアを計算する
    score_list = np.array(score_list)
    average_score = np.average(score_list)
    print("logistic_score:", average_score)

    return pd.DataFrame([average_score], columns = ["score"])