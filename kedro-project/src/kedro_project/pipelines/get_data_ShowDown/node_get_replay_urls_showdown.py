from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
import time
import pandas as pd


def get_replay_urls():
    # ルールを指定する
    rule = "[Gen 8] Battle Stadium Singles"

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

    # 指定したURLに遷移
    driver.get("https://replay.pokemonshowdown.com/")

    # print(driver.page_source)

    # ルールを入力する
    form = driver.find_element_by_xpath("/html/body/div[2]/div/form[2]/p/label/input")

    # フォームを入力する
    form.send_keys(rule)

    # クリックする
    driver.find_element_by_xpath("/html/body/div[2]/div/form[2]/p/button").click()

    # 一秒待機
    time.sleep(1)
    count = 0

    for i in range(30):
        try:
            driver.find_element_by_xpath("/html/body/div[2]/div/p/button").click()
            # 一秒待機
            time.sleep(2)
            count += 1
            print(count)
        except:
            break

    # リンクを取得する
    # aタグのhrefをelementでリスト化
    elements = driver.find_elements_by_xpath("//a[@href]")

    # リプレイに関するurlのみ抽出する(8個目以降を取る)
    url_list = []
    for element in elements:
        url_list.append(element.get_attribute("href"))

    replay_urls = pd.DataFrame(url_list[8:], columns= ["url"])

    # Chromeを終了
    driver.quit()

    return replay_urls


"""
if __name__ == "__main__":
    # リプレイのurlを取得する
    replay_urls = get_replay_urls()
    # リプレイのurlをcsvで出力する
    replay_urls.to_csv("get_showdown_data/data/replay_urls.csv", index=False)
"""