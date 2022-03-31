import pandas as pd

def make_frequent_pokemon_data(dark_urshifu_df, water_urshifu_df):
    """
    出現したポケモンのリストを作る。一回しか出てこないポケモンは除外する
    """
    # 悪・水ウーラオスデータに関して、ポケモンの出現回数を計算する
    dark_count_df = pd.DataFrame(count_pokemon(dark_urshifu_df))
    water_count_df = pd.DataFrame(count_pokemon(water_urshifu_df))
    
    # 出現回数が少ない（一回）ポケモンは足切りした上で、出現ポケモンのベクトル（DataFrame）を作る
    ## 悪・水ウーラオスのデータを結合する
    merged_count_df = pd.concat([dark_count_df, water_count_df], axis = 1)
    merged_count_df.columns = ["dark", "water"]
    merged_count_df = merged_count_df.fillna(0)
    merged_count_df["sum_count"] = merged_count_df["dark"] + merged_count_df["water"]

    ## 足切りする
    frequent_pokemon_df = merged_count_df[merged_count_df["sum_count"] >= 2]
    frequent_pokemon_df = pd.DataFrame(frequent_pokemon_df.index, columns=["name"])
    print(frequent_pokemon_df)
    return frequent_pokemon_df

def count_pokemon(df):
    """
    ポケモンの出現回数をカウントする。
    Augs
        df:元データ(raw_dark_urshifu_data, raw_water_urshifu_dataを想定)
    Returns
        count_df:indexがポケモン名、value列が出現回数を意味するdataframe
    """
    # ポケモンのデータのみ抽出し、縦のベクトルにする
    poke_vec = df.iloc[:, 0:6]
    count_df = poke_vec.melt()["value"].value_counts()
    
    #各ポケモンの出現回数を調べる
    return count_df