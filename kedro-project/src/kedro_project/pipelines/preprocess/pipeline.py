"""Example code for the nodes in the example pipeline. This code is meant
just for illustrating basic Kedro features.

Delete this when you start working on your own Kedro project.
"""

from heapq import merge
from kedro.pipeline import Pipeline, node

from .node_calc_opponent_weakness import calc_opponent_weakness
from .node_merge_raw_data import merge_raw_data
from .node_make_used_pokemon_features import make_used_pokemon_features
from .node_make_used_type_features import make_used_type_features
from .node_merge_features import merge_features

def create_pipeline(**kwargs):
    return Pipeline(
        [      
            node(
                calc_opponent_weakness,
                ["raw_opponent_pokemon", "raw_pokemon_data_sheet", "raw_type_compatibility"],
                "intermediate_opponent_compatibility"
            ), 
            node(
                merge_raw_data,
                ["raw_dark_urshifu_data", "raw_water_urshifu_data"],
                "primary_merged_data"
            ), 
            node(
                make_used_pokemon_features,
                ["primary_merged_data", "params:param_freq_threshold"],
                "feature_used_pokemon"
            ),
            node(
                make_used_type_features,
                ["primary_merged_data", "raw_pokemon_data_sheet"],
                "feature_type_frequency"
            ), 
            node(
                merge_features,
                ["feature_used_pokemon", "feature_type_frequency"],
                "model_input_feature_merged_data"
            ),

        ]
    )

