"""
結果を結合する
"""

import pandas as pd

def merge_result(result_gbdt, result_cnn, result_logistic):
    merged_df = pd.concat([result_gbdt, result_cnn, result_logistic])
    merged_df.index = ["gbdt", "cnn", "logistic"]
    return merged_df