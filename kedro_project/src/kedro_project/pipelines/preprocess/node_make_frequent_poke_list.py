import pandas as pd

def make_frequent_pokemon_list(merged_df, param_freq_threshold):
    """
    出現したポケモンのリストを作る。出現回数が閾値を超えないポケモンは除外する。
    Augs
        merged_df:悪、水ウーラオスのデータを結合したもの
    Returns
        frequent_pokemon_df:indexがポケモン名、value列が出現回数を意味するdataframe
    """
    # ポケモンの出現回数を計算する    
    ## ポケモンのデータのみ抽出し、縦のベクトルにする
    poke_vec = merged_df.iloc[:, 0:6]
    count_df = pd.DataFrame(poke_vec.melt()["value"].value_counts())
    
    # 出現回数が少ないポケモンは足切りした上で、出現ポケモンのベクトル（DataFrame）を作る
    frequent_pokemon_df = count_df[count_df["value"] >= param_freq_threshold]
    
    frequent_pokemon_list = list(frequent_pokemon_df.index)
    # df形式にして保存
    frequent_pokemon_df = pd.DataFrame(frequent_pokemon_list, columns=["name"])
    return frequent_pokemon_df