"""
light gbmを使って、gbdtモデルの二値分類を行う。
尚、評価に当たってはクロスバリデーション（n = 5）で行う。
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
import lightgbm as lgb

def train_gbdt(df, pram_gbdt_max_bin, pram_gbdt_num_leaves):
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
        
        """
        print(f"fold_id: {fold_id}")
        print(f"train_y y == 1 rate: {sum(train_y / len(train_y))}")
        print(f"test_y y == 1 rate:, {sum(test_y / len(test_y))}")
        """
    
        # 学習
        lgb_train = lgb.Dataset(train_x, train_y)

        # 検証
        lgb_test = lgb.Dataset(test_x, test_y, reference=lgb_train)
        params = {
            "objective": "binary",
            "max_bin": pram_gbdt_max_bin,
            "num_leaves": pram_gbdt_num_leaves
        }
        model = lgb.train(params, 
        lgb_train, 
        valid_sets=[lgb_train, lgb_test],
        verbose_eval=10, 
        num_boost_round=1000, 
        early_stopping_rounds=10)

        pred_y = model.predict(test_x, num_iteration=model.best_iteration)

        # 値を離散値に変換し、スコアを計算、保存する
        pred_y = (pred_y > 0.5).astype(int)
        score = (sum(pred_y == test_y) / len(test_y))
        score_list.append(score)
        
        """
        # 重要度を出力する
        importance = pd.DataFrame(model.feature_importance(), index = x.columns, columns=['importance'])
        print(importance)
        """
        
    # 平均スコアを計算する
    score_list = np.array(score_list)
    average_score = np.average(score_list)
    print("gbdt_score:", average_score)

    return None