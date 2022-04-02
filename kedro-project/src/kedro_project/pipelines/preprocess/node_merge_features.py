import pandas as pd

def merge_features(used_pokemon, type_frequency, opponent_advantage, params):
    merged = pd.DataFrame([])

    if params["use_feature_used_pokemon"]:
        merged = pd.concat([merged, used_pokemon], axis=1)

    if params["use_feature_type_frequency"]:
        merged = pd.concat([merged, type_frequency], axis=1)

    if params["use_feature_opponent_advantage"]:
        merged = pd.concat([merged, opponent_advantage], axis=1)

    return merged