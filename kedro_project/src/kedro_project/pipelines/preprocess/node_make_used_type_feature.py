import pandas as pd

def make_used_type_feature(merged_df, pokemon_data_sheet):
    """
    タイプの出現頻度を計算し、DataFrame形式で出力する
    """
    # 全ポケモンのタイプに関するDataFrameを作る
    pokemon_type_df = pokemon_data_sheet[["名前", "タイプ1", "タイプ2"]]

    # タイプ一覧を取得し、辞書を作成する
    type_name = pokemon_type_df["タイプ1"].unique()
    
    #
    type_frequency_list = []

    for data in merged_df.itertuples():
        # 構築毎にデータを取り出す
        ## 使用数をカウントする辞書をリセットする
        type_count_dict = dict(zip(type_name, [0] * len(type_name)))

        for i in range(1, 7):
            poke = data[i]
            type_count_dict = update_type_count_dict(type_count_dict, poke, pokemon_type_df)
    
        # 構築で使用されているタイプに関するリストを取得
        used_type = list(type_count_dict.values())
        type_frequency_list.append(used_type)
    
    # DataFrameに変換する
    type_frequency_df = pd.DataFrame(type_frequency_list, columns = type_name)
    
    return type_frequency_df

def update_type_count_dict(type_count_dict, poke, pokemon_type_df):
    """
    タイプに関する辞書とポケモン名を受け取って、辞書を更新する関数
    """
    if poke in ["ウーラオス悪", "ウーラオス水"]:
        return type_count_dict

    # 出現ポケモンに関する行を取得する
    specified_poke_raw = pokemon_type_df[pokemon_type_df["名前"] == poke]
    # タイプを取得する
    type1 = specified_poke_raw["タイプ1"].iloc[0]
    type2 = specified_poke_raw["タイプ2"].iloc[0]

    type_count_dict[type1] += 1
    # タイプ２が存在する場合はそれも追加する
    if not pd.isna(type2):
        type_count_dict[type2] += 1
        
    return type_count_dict