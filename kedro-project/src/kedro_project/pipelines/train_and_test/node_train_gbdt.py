"""
light gbmを使って、gbdtモデルの二値分類を行う。
尚、評価に当たってはクロスバリデーション（n = 5）を行い、平均スコアを計算する。

また、特徴量の重要度も計算し、出力する。
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
import lightgbm as lgb

def train_gbdt(train_x, train_y, test_x, test_y, pram_gbdt_max_bin, pram_gbdt_num_leaves):
    # test_yをnp.arrayに変換しておく
    test_y = np.array(test_y.iloc[:, 0])
    # クロスバリデーションの設定
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
    
    score_list = []
    importance_df = pd.DataFrame([])

    for fold_id, (train_index, valid_index) in enumerate(cv.split(train_x, train_y)):
        # 学習データと検証データに分割する
        train_cv_x = train_x.iloc[train_index, : ]
        valid_x = train_x.iloc[valid_index, : ]
        train_cv_y = train_y.iloc[train_index]
        valid_y = train_y.iloc[valid_index]
    
        # 学習
        ## light gbm用に学習、検証データを指定する
        lgb_train = lgb.Dataset(train_cv_x, train_cv_y)
        lgb_valid = lgb.Dataset(valid_x, valid_y, reference=lgb_train)

        params = {
            "objective": "binary",
            "max_bin": pram_gbdt_max_bin,
            "num_leaves": pram_gbdt_num_leaves
        }
        model = lgb.train(params, 
        lgb_train, 
        valid_sets=[lgb_train, lgb_valid],
        verbose_eval=False,
        num_boost_round=1000, 
        early_stopping_rounds=10)

        # 検証
        pred_y = model.predict(test_x, num_iteration=model.best_iteration)

        # 値を離散値に変換し、スコアを計算、保存する
        pred_y = (pred_y > 0.5).astype(int)

        score = sum(pred_y == test_y) / len(test_y)
        score_list.append(score)

        # 重要度を計算する
        tmp_importance_df = pd.DataFrame(model.feature_importance(), index = train_x.columns)
        importance_df = pd.concat([importance_df, tmp_importance_df], axis=1)


    # 平均重要度を計算し、降順に並び変える
    importance_df = pd.DataFrame(importance_df.mean(axis = "columns"), columns = ["importance"])
    importance_df = importance_df.sort_values("importance", ascending= False)

    # 平均スコアを計算する
    score_list = np.array(score_list)
    average_score = np.average(score_list)
    print("gbdt_score:", average_score)
    
    return pd.DataFrame([average_score], columns = ["score"]), importance_df

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