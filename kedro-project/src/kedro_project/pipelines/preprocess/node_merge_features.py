import pandas as pd

def merge_features(one_hot_data, type_features):
    merged = pd.concat([one_hot_data, type_features], axis=1)

    return merged