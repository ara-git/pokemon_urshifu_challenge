"""
ポケットファンクション（https://nouthuca.com/）からウーラオス入り構築の情報をスクレイピングする。
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
import time
import pandas as pd
import re

def get_party_data(url):
    # ChromeOptionsを設定
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument('--proxy-server="direct://"')
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument("--kiosk")
    # chromeを開かない
    options.add_argument("--headless")

    # Chromeを起動
    print("Chromeを起動中...")
    driver = webdriver.Chrome(options=options)

    # データ（構築）の数を調べる
    # 指定したURLに遷移
    driver.get(url)

    # 数字のみ抽出する
    num_of_party = driver.find_element_by_xpath(
        "/html/body/div[1]/main/div[2]/ul[1]/li[1]"
    ).text
    num_of_party = re.findall(r"\d+", num_of_party)
    num_of_party = int(".".join(num_of_party))
    print("num:", num_of_party)

    # 結果の格納先
    party_list = []

    # ページのカウント
    page_count = 0

    while len(party_list) < num_of_party:
        # ページカウントを増やす
        page_count += 1
        # 指定したURLに遷移
        driver.get(url + "&num=" + str(page_count))
        # 構築の情報を読み込み、リスト形式で保存する
        elements = driver.find_elements_by_class_name("party")

        for elem in elements:
            tmp_list = []
            # ポケモン名を抽出する
            poke_list = list(elem.find_elements_by_class_name("pokemon"))
            # altタグ（ポケモン、道具の名前）を取得する
            tmp_list += list(map(lambda x: x.get_attribute("alt"), poke_list))

            # 道具名を抽出する
            item_list = list(elem.find_elements_by_class_name("item"))
            # altタグ（ポケモン、道具の名前）を取得する
            tmp_list += list(map(lambda x: x.get_attribute("alt"), item_list))

            party_list.append(tmp_list)

        # 次のページへ
        time.sleep(3)
        print("number of party:", len(party_list))

    # Chromeを終了
    driver.quit()

    party_df = pd.DataFrame(
        party_list,
        columns=[
            "p1",
            "p2",
            "p3",
            "p4",
            "p5",
            "p6",
            "i1",
            "i2",
            "i3",
            "i4",
            "i5",
            "i6",
        ],
    )

    return party_df

def main(dark_urshifu_url, water_urshifu_url):
    dark_urshifu_df = get_party_data(dark_urshifu_url)
    water_urshifu_df = get_party_data(water_urshifu_url)

    return dark_urshifu_df, water_urshifu_df
