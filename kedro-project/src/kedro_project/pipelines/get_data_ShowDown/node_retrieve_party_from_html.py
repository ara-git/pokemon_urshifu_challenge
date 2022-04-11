import bs4
import pandas as pd
import glob

def retrieve_party_from_html(htmls, poke_data_sheet_df):
    """
    DLしたローカルのhtmlファイル（showdownの対戦リプレイデータ）から、ウーラオス入りの構築データを取得する。
    Augs:
        htmls: Kedroが上手く動くための空のファイル（使わない）
        poke_data_sheet_df: ポケモンの英名、日本語名を変換するためのデータ
    Returns:
        dark_urshifu_party_df: 悪ウーラオス入り構築のデータ
        water_urshifu_party_df: 水ウーラオス入り構築のデータ
    """
    poke_name_jp_en_dict = dict(zip(poke_data_sheet_df["英語名"], poke_data_sheet_df["名前"]))

    # フォルダ内部のファイル一覧を取得する
    files_list = glob.glob("data/01_raw/ShowDown_htmls/*")
    dark_urshifu_party_list = []
    water_urshifu_party_list = []

    for i in range(len(files_list)):
        # ファイルを開く
        soup = bs4.BeautifulSoup(open(files_list[i], encoding= "utf-8"), 'html.parser')
        # バトルデータのstringを読み込む
        battle_log_str = soup.find("script", class_="battle-log-data").string

        if "p1a: Urshifu|Urshifu-Rapid-Strike" in battle_log_str:
            # 自構築に水ウーラオスが入っている場合
            party_data = get_party_data_from_html(poke_name_jp_en_dict, battle_log_str, side = "my", urshifu_type = "water")
            ## ポケモン数が6の時のみ保存する
            if len(party_data) == 6:
                water_urshifu_party_list.append(party_data)

        elif "p1a: Urshifu|Urshifu" in battle_log_str:
            # 自構築に悪ウーラオスが入っている場合
            party_data = get_party_data_from_html(poke_name_jp_en_dict, battle_log_str, side = "my", urshifu_type = "dark")
            ## ポケモン数が6の時のみ保存する
            if len(party_data) == 6:
                dark_urshifu_party_list.append(party_data)

        if "p2a: Urshifu|Urshifu-Rapid-Strike" in battle_log_str:
            # 相手構築に水ウーラオスが入っている場合
            party_data = get_party_data_from_html(poke_name_jp_en_dict, battle_log_str, side = "opponent", urshifu_type = "water")
            ## ポケモン数が6の時のみ保存する
            if len(party_data) == 6:
                water_urshifu_party_list.append(party_data)

        elif "p2a: Urshifu|Urshifu" in battle_log_str:
            # 相手構築に悪ウーラオスが入っている場合
            party_data = get_party_data_from_html(poke_name_jp_en_dict, battle_log_str, side = "opponent", urshifu_type = "dark")
            ## ポケモン数が6の時のみ保存する
            if len(party_data) == 6:
                dark_urshifu_party_list.append(party_data)

    dark_urshifu_party_df = pd.DataFrame(dark_urshifu_party_list, columns = ["p1", "p2", "p3", "p4", "p5", "p6"])
    water_urshifu_party_df = pd.DataFrame(water_urshifu_party_list, columns = ["p1", "p2", "p3", "p4", "p5", "p6"])

    print(dark_urshifu_party_df)
    print(water_urshifu_party_df)

    return dark_urshifu_party_df, water_urshifu_party_df


def get_party_data_from_html(poke_name_jp_en_dict, battle_log_str, side, urshifu_type):
    """
    バトルデータのstringから構築のリストを抽出する
    Augs:
        poke_name_jp_en_dict: ポケモン名が一対一で対応するような辞書。キーが英語名、値が日本語名になっている。
        battle_log_str:対戦データのstring
        side:抽出したい構築が自分("my")か相手か("opponent")
        urshifu_type:抽出したいウーラオスのタイプ("dark" or "water")
    """
    if side == "my":
        # 自構築を抜き出す
        party_list = [x.split(",")[0][9:] for x in battle_log_str.split("\n") if "|poke|p1|" in x]
    elif side == "opponent":
        # 相手構築を抜き出す
        party_list = [x.split(",")[0][9:] for x in battle_log_str.split("\n") if "|poke|p2|" in x]

    # ウーラオス要素を削除する（５体にする）
    party_list.remove("Urshifu-*")
    # 名称を日本語に変更する
    party_list = list(map(lambda eng_name: poke_name_jp_en_dict[eng_name], party_list))

    # ウーラオス要素を追加する
    if urshifu_type == "dark":
        party_list.append("ウーラオス悪")
    elif urshifu_type == "water":
        party_list.append("ウーラオス水")

    return party_list