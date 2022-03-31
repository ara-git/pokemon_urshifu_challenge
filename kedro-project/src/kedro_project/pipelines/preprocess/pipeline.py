"""Example code for the nodes in the example pipeline. This code is meant
just for illustrating basic Kedro features.

Delete this when you start working on your own Kedro project.
"""

from kedro.pipeline import Pipeline, node

from .node_preprocess import preprocess
from .node_make_frequent_pokemon_data import make_frequent_pokemon_data

def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                make_frequent_pokemon_data,
                ["raw_dark_urshifu_data", "raw_water_urshifu_data"],
                "intermediate_frequent_pokemon_data"
            ),
            node(
                preprocess,
                ["raw_dark_urshifu_data", "raw_water_urshifu_data", "intermediate_frequent_pokemon_data"],
                "intermediate_preprocessed_data"
            ),
        ]
    )

