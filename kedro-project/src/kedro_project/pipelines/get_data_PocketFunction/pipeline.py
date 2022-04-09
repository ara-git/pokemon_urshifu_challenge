from kedro.pipeline import Pipeline, node
from .node_get_data_PocketFunction import main

def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                main,
                ["params:dark_urshifu_url", "params:water_urshifu_url"],
                ["raw_dark_urshifu_data", "raw_water_urshifu_data"],
                name="get_data_set_from_PocketFunction",
            ),
        ]
    )
