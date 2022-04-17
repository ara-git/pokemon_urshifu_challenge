import pandas as pd

def merge_features(used_pokemon, type_frequency, opponent_advantage, selected_feature_name_df , params):
    """
    特徴量の列を結合する　
    """
    merged = pd.DataFrame([])

    if params["use_feature_used_pokemon"]:
        merged = pd.concat([merged, used_pokemon], axis=1)

    if params["use_feature_type_frequency"]:
        # [0, 1]で収まるように標準化する
        # type_frequency = type_frequency / type_frequency.max()
        merged = pd.concat([merged, type_frequency], axis=1)

    if params["use_feature_opponent_advantage"]:
        # [0, 1]で収まるように標準化する
        # opponent_advantage = opponent_advantage / opponent_advantage.max()
        merged = pd.concat([merged, opponent_advantage], axis=1)

    # 使う特徴量を抽出する(パラメータでするかしないか決める)
    if params["use_selected_features"]:
        selected_feature_name_list = list(selected_feature_name_df.iloc[:, 0])
        merged = merged[["target"] + selected_feature_name_list]

    return merged