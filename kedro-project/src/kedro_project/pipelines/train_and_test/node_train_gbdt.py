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

    return pd.DataFrame([average_score], columns = ["score"])

"""
def train_GBDT(train_x, train_y,test_x, test_y, params_learning_rate_gbdt, params_max_depth_gbdt):
    # ハイパーパラメータを指定して学習実行
    train_params = {
        'objective': 'binary:logistic',
        'eval_metric': 'logloss',
        'learning_rate': params_learning_rate_gbdt,
        'max_depth': params_max_depth_gbdt,
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

    print(booster.get_fscore())
    print("GBDT_score", acc)

    # 出力(2): 特徴量の重要度を描画
    _, ax = plt.subplots(figsize=(12, 12))
    xgb.plot_importance(booster,
                        ax=ax,
                        importance_type='gain',
                        show_values=False)
    
    plt.show()
    return pd.DataFrame(["GBDT_score", acc])
"""