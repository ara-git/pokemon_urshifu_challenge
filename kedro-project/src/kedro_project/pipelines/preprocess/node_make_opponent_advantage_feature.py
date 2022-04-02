import pandas as pd
import numpy as np

def make_opponent_advantage_features(type_frequency_df, opponent_compatibility_df):
    """
    仮想敵（上位ポケモン）に対する有利度合いを計算する。
    具体的には、攻めのタイプ相性を計算する。
    """
    # 二つのdfの列順をそろえる
    type_frequency_df = type_frequency_df[list(opponent_compatibility_df.columns[1:])]

    # 自パーティを一つずつ取り出し、仮想敵に対する有利度を計算する
    opponent_advantage_list = []
    for data in type_frequency_df.itertuples():
        party_type_count_raw = np.array(data[1:])

        # 仮想敵でイテレート
        tmp_list = []
        for data in opponent_compatibility_df.itertuples():
            opponent_comatibility_raw = np.array(data[2:])
            advantage_point = opponent_comatibility_raw.dot(party_type_count_raw)
            
            tmp_list.append(advantage_point)
        
        opponent_advantage_list.append(tmp_list)

    # 列名は"vsポケモン名"としてDataFrameを作成する
    opponent_advantage_df = pd.DataFrame(opponent_advantage_list, columns=list(map(lambda poke:"vs" + poke , opponent_compatibility_df["Unnamed: 0"])))

    return opponent_advantage_df