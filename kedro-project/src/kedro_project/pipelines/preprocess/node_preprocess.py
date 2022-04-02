import pandas as pd

def make_used_pokemon_features(merged_df, param_freq_threshold):
    """
    使用したポケモンに関する、シンプルなone-hotデータに変換する。
    ただし、低頻出（一回以下）ポケモンのデータは使わない。
    
    Augs
        merged_data:悪、水ウーラオスのパーティデータ
        frequent_pokemon_data:高頻出（2回以上）ポケモンの名前が入ったDataFrame
    Returns
        one_hot_df:パーティで使用しているポケモンの情報のみが入ったシンプルなone-hot
    """
    # 高頻出ポケモンのリストを作成し、それに関する辞書を作成する    
    frequent_list = make_frequent_pokemon_data(merged_df, param_freq_threshold)
    one_hot_dict = dict(zip(frequent_list, [0] * len(frequent_list)))

    one_hot_list = []
    ## DataFrameを一行ずつ取り出す
    for raw in merged_df.itertuples():
        #辞書の値を０に戻す
        one_hot_dict = one_hot_dict.fromkeys(frequent_list, 0)

        for i in range(6):
            poke_name = raw[i + 1]
            if poke_name in one_hot_dict.keys():
                # キーが存在する（ある程度頻出）のポケモンのみ抽出する
                one_hot_dict[poke_name] = 1

        one_hot_list.append(list(one_hot_dict.values()))

    one_hot_df = pd.DataFrame(one_hot_list, columns = frequent_list)

    # 列名を変更する
    one_hot_df = one_hot_df.rename(columns={"ウーラオス悪": "target"})
    # 不要列を削除する
    del one_hot_df["ウーラオス水"]

    return one_hot_df

def make_frequent_pokemon_data(merged_df, param_freq_threshold):
    """
    出現したポケモンのリストを作る。一回しか出てこないポケモンは除外する。
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
    return frequent_pokemon_list
