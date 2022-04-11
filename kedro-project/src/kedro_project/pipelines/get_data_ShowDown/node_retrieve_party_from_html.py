import bs4
import pandas as pd
import glob

def retrieve_party_from_html(htmls, poke_data_sheet_df):
    poke_name_jp_en_dict = dict(zip(poke_data_sheet_df["英語名"], poke_data_sheet_df["名前"]))

    # フォルダ内部のファイル一覧を取得する
    files_list = glob.glob("data/01_raw/ShowDown_htmls/*")
    dark_urshifu_party_list = []
    water_urshifu_party_list = []
    
    soup = bs4.BeautifulSoup(open(r'C:\Users\ara-d\pokemon_urshifu_challenge\get_showdown_data\data\replay_htmls\Gen8BattleStadiumSingles-2022-04-04-akingofsand-bllkz.html', encoding= "utf-8"), 'html.parser')


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

if __name__ == "__main__":
    poke_data_sheet_df = pd.read_csv(r"C:\Users\ara-d\pokemon_urshifu_challenge\kedro-project\data\01_raw\pokemon_data_sheet.csv")
    print(poke_data_sheet_df)
    retrieve_party_from_html(None, poke_data_sheet_df)