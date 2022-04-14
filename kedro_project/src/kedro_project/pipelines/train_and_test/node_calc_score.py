"""
予測値と実際の値の乖離度を計算し、各モデルのスコアを算出する。
"""
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score

def calc_score(test_y, pred_gbdt_df, pred_cnn_df, pred_logistic_df):
    score_gbdt_list = []
    score_cnn_list = []
    score_logistic_list = []
    score_ensemble_list = []

    for i in range(5):
        """
        各モデルのスコアを計算する。

        予測値の数（= closs validationの個数 = 5）だけiteration
        """
        # 予測値を一列ずつ取り出し、一つのdfにまとめる
        pred_y_gbdt = pred_gbdt_df.iloc[:, i]
        pred_y_cnn = pred_cnn_df.iloc[:, i]
        pred_y_logistic = pred_logistic_df.iloc[:, i]
        pred_df = pd.concat([pred_y_gbdt, pred_y_cnn, pred_y_logistic], axis = 1)
        pred_df.columns = ["gbdt", "cnn", "logistic"]

        ## アンサンブルも計算し、列追加する
        pred_df["ensemble"] = list(pred_df.sum(axis = 1))
        pred_df["ensemble"] = list((pred_df["ensemble"] >= 2).astype(int))

        # 予測スコアを計算する
        score_gbdt = accuracy_score(test_y, pred_df["gbdt"])
        score_cnn = accuracy_score(test_y, pred_df["cnn"])
        score_logistic = accuracy_score(test_y, pred_df["logistic"])
        score_emsemble = accuracy_score(test_y, pred_df["ensemble"])
        
        # 結果を保存する
        score_gbdt_list.append(score_gbdt)
        score_cnn_list.append(score_cnn)
        score_logistic_list.append(score_logistic)
        score_ensemble_list.append(score_emsemble)

    # 各モデルの平均スコアを計算する
    mean_score_gbdt = np.mean(score_gbdt_list)
    mean_score_cnn = np.mean(score_cnn_list)
    mean_score_logistic = np.mean(score_logistic_list)
    mean_score_ensemble = np.mean(score_ensemble_list)
    
    score_result_df = pd.DataFrame([
        mean_score_gbdt,
        mean_score_cnn,
        mean_score_logistic,
        mean_score_ensemble],
        columns = ["mean score"],  
        index = ["gbdt", "cnn", "logistic", "ensemble"])

    return score_result_df