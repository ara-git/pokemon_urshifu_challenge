"""
showdownから対戦データをDLし、ウーラオス構築のデータを取得する。流れとしては、
1. 対戦リプレイのurlリストを取得する。（get_replay_urls）
2. urlにアクセスし、対戦リプレイのhtmlデータをDLする。
3. ローカルのhtmlファイルから、ウーラオス入りの構築データを抽出し、csv形式にして出力する。

尚、1, 2から行うと実行時間がとても長くなってしまうので、基本的（デフォルトでは）なKedro runでは3から行う事にする。

1, 2から行いたい場合は環境変数を以下の様に設定するとよい。
- 1から実行したい場合: 環境変数"get_data_sd_url"に"True"を代入する。
- 2から実行したい場合: 環境変数"get_data_sd_download_html"に"True"を代入する。
"""
from kedro.pipeline import Pipeline, node
import os

from .node_get_replay_urls_showdown import get_replay_urls
from .node_download_replay_html_from_showdown import download_replay_html_from_showdown
from .node_retrieve_party_from_html import retrieve_party_from_html

def create_pipeline(**kwargs):
    if os.environ.get("get_data_sd_get_url") == "True":
        # url取得から全て行う場合
        return Pipeline(
            [   node(
                get_replay_urls,
                inputs=None,
                outputs="raw_replay_urls_ShowDown"
                ),
                node(
                    download_replay_html_from_showdown,
                    inputs="raw_replay_urls_ShowDown",
                    outputs="raw_htmls"
                ),
                node(
                    retrieve_party_from_html,
                    inputs=["raw_htmls", "raw_pokemon_data_sheet"],
                    outputs = ["raw_dark_urshifu_data_sd", "raw_water_urshifu_data_sd"]
                ),
            ]
        )
    elif os.environ.get("get_data_sd_download_html") == "True":
        # url取得を省略し、htmlの取得（スクレイピング）から行う場合
            return Pipeline(
            [
                node(
                    download_replay_html_from_showdown,
                    inputs="raw_replay_urls_ShowDown",
                    outputs="raw_htmls"
                ),
                node(
                    retrieve_party_from_html,
                    inputs=["raw_htmls", "raw_pokemon_data_sheet"],
                    outputs = ["raw_dark_urshifu_data_sd", "raw_water_urshifu_data_sd"]
                ),
            ]
        )
    elif os.environ.get("get_data_sd_read_html") == "True":
        # htmlファイルから構築情報の抽出のみ行う。
            return Pipeline(
            [
                node(
                    retrieve_party_from_html,
                    inputs=["raw_htmls", "raw_pokemon_data_sheet"],
                    outputs = ["raw_dark_urshifu_data_sd", "raw_water_urshifu_data_sd"]
                ),
            ]
        )