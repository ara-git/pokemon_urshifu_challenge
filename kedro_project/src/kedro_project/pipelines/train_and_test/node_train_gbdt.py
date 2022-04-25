"""
light gbmを使って、gbdtモデルの二値分類を行う。
尚、評価に当たってはクロスバリデーション（n = 5）を行い、平均スコアを計算する。

また、特徴量の重要度も計算し、出力する。
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
import lightgbm as lgb

# LightGBMおよび交差検定用
from sklearn.model_selection import KFold
import optuna.integration.lightgbm as lgb

def train_gbdt(train_x, train_y, test_x, pram_gbdt_max_bin, pram_gbdt_num_leaves):
    """
    まずoptunaでハイパラをチューニングし、それを使ってtestデータを予測する。
    尚、cvで分割し、平均スコアを計算する。
    """
    # ハイパーパラメータサーチ&モデル構築
    params = {'objective': "binary",
            'metric': 'rmse',
            'random_seed':0} 

    # LightGBM用のデータセットに変換
    lgb_train = lgb.Dataset(train_x, train_y)

    # クロスバリデーションによるハイパーパラメータの探索 3fold
    tuner = lgb.LightGBMTunerCV(params, lgb_train, verbose_eval=100, early_stopping_rounds=100, folds=KFold(n_splits=5))

    # ハイパーパラメータ探索の実行
    tuner.run()

    # サーチしたパラメータの表示
    best_params = tuner.best_params
    print("  Params: ")
    for key, value in best_params.items():
        print("    {}: {}".format(key, value))

    # ここから改めて学習を行う
    ## クロスバリデーションの設定
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
    
    importance_df = pd.DataFrame([])

    pred_y_list = []
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
        model = lgb.train(best_params, 
        lgb_train, 
        valid_sets=[lgb_train, lgb_valid],
        verbose_eval=False,
        num_boost_round=1000, 
        early_stopping_rounds=10)

        # 検証
        pred_y = model.predict(test_x, num_iteration=model.best_iteration)

        # 値を離散値に変換し、スコアを計算、保存する
        pred_y = list((pred_y > 0.5).astype(int))

        pred_y_list.append(pred_y)
        
        # 重要度を計算する
        tmp_importance_df = pd.DataFrame(model.feature_importance(), index = train_x.columns)
        importance_df = pd.concat([importance_df, tmp_importance_df], axis=1)

    # dataframeに変更する
    pred_y_df = pd.DataFrame(pred_y_list).T
    pred_y_df.columns = ["pred"] * len(pred_y_df.columns)

    # 平均重要度を計算し、降順に並び変える
    importance_df = pd.DataFrame(importance_df.mean(axis = "columns"), columns = ["importance"])
    importance_df = importance_df.sort_values("importance", ascending= False)

    # return pd.DataFrame([]), pd.DataFrame([])
    return pred_y_df, importance_df