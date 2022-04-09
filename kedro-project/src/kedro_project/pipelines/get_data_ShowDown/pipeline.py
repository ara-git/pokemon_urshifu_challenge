from kedro.pipeline import Pipeline, node

from .node_get_replay_urls_showdown import get_replay_urls
from .node_download_replay_html_from_showdown import download_replay_html_from_showdown
from .node_retrieve_party_from_html import retrieve_party_from_html


def create_pipeline(**kwargs):
    """
    url取得を省略したバージョン(デバッグ)
    """
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
    """
    return Pipeline(
        [   
            node(
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
    """