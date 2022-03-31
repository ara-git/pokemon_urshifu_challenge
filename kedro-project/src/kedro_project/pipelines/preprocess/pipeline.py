"""Example code for the nodes in the example pipeline. This code is meant
just for illustrating basic Kedro features.

Delete this when you start working on your own Kedro project.
"""

from kedro.pipeline import Pipeline, node

from .node_make_frequent_pokemon_data import make_frequent_pokemon_data
from .node_preprocess import merge_data
from .node_preprocess import convert_one_hot


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                merge_data,
                ["raw_dark_urshifu_data", "raw_water_urshifu_data"],
                "intermediate_merged_data"
            ), 
            node(
                make_frequent_pokemon_data,
                ["intermediate_merged_data", "params:param_freq_threshold"],
                "intermediate_frequent_pokemon_data"
            ),
            node(
                convert_one_hot,
                ["intermediate_merged_data", "intermediate_frequent_pokemon_data"],
                "primary_one_hot_data"
            ),
        ]
    )

