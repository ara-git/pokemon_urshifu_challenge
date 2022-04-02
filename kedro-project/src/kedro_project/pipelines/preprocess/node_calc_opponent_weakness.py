import pandas as pd
import numpy as np

def calc_opponent_weakness(opponent_pokemon_df, pokemon_data_sheet, type_compatibility_df):
    """
    仮想敵の弱点タイプを計算し、DataFrameで出力する。
    Augs
        opponent_pokemon_df:分析対象とする仮想敵のリスト
        pokemon_data_sheet:全ポケモンに関するデータ、仮想敵のタイプを調べるのに使う。
        type_comatibility_df:タイプ相性表
    Returns
        opponent_compatibility_df:仮想敵の（防御に関する）タイプ相性表
    """    
    # タイプ相性表を加工する
    ## 記号を数字で置き換える
    type_compatibility_df = type_compatibility_df.replace("●", 1)
    type_compatibility_df = type_compatibility_df.replace("▲", -1)
    type_compatibility_df = type_compatibility_df.replace("×", -100)
    type_compatibility_df = type_compatibility_df.fillna(0)

    # 仮想敵のリストを作成
    opponent_pokemon_list = list(opponent_pokemon_df["name"])

    # 全ポケモンのタイプに関するDataFrameを作る
    pokemon_type_df = pokemon_data_sheet[["名前", "タイプ1", "タイプ2"]]

    # 仮想敵の相性を計算する
    result_list = []
    for poke in opponent_pokemon_list:
        # 仮想敵に関する行を取得する
        specified_poke_raw = pokemon_type_df[pokemon_type_df["名前"] == poke]
        # タイプを取得する
        type1 = specified_poke_raw["タイプ1"].iloc[0]
        type2 = specified_poke_raw["タイプ2"].iloc[0]

        # タイプ１に関する相性を計算し、np.array形式で保存する
        type1_compatibility = np.array(type_compatibility_df[type1])

        if not pd.isna(type2):
            # タイプ２が存在する場合、タイプ２に関する相性を計算する
            type2_compatibility = np.array(type_compatibility_df[type2])
            specified_type_compatibility_array = type1_compatibility + type2_compatibility
        else:
            # しない場合、計算しない
            specified_type_compatibility_array = type1_compatibility
        result_list.append(specified_type_compatibility_array)

    # DataFrame形式に変更
    opponent_compatibility_df = pd.DataFrame(result_list, columns=type_compatibility_df["Unnamed: 0"], index=opponent_pokemon_list)

    # 無効は半減と同じように-1とする
    opponent_compatibility_df.where(opponent_compatibility_df >= -1, "-1", inplace= True)

    return opponent_compatibility_df