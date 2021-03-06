"""Example code for the nodes in the example pipeline. This code is meant
just for illustrating basic Kedro features.

Delete this when you start working on your own Kedro project.
"""

from heapq import merge
from kedro.pipeline import Pipeline, node

from .node_calc_opponent_weakness import calc_opponent_weakness
from .node_merge_raw_data import merge_raw_data
from .node_make_frequent_poke_list import make_frequent_pokemon_list
from .node_make_used_pokemon_feature import make_used_pokemon_feature
from .node_make_used_type_feature import make_used_type_feature
from .node_merge_features import merge_features
from .node_make_opponent_advantage_feature import make_opponent_advantage_feature

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
                ["raw_dark_urshifu_data", "raw_water_urshifu_data", "raw_dark_urshifu_data_sd", "raw_water_urshifu_data_sd"],
                "primary_merged_data"
            ), 
            node(
                make_frequent_pokemon_list,
                ["primary_merged_data", "params:param_freq_threshold"],
                "intermediate_frequent_pokemon_list"
            ),
            node(
                make_used_pokemon_feature,
                ["primary_merged_data", "intermediate_frequent_pokemon_list"],
                "feature_used_pokemon"
            ),
            node(
                make_used_type_feature,
                ["primary_merged_data", "raw_pokemon_data_sheet"],
                "feature_type_frequency"
            ),
            node(
                make_opponent_advantage_feature,
                ["feature_type_frequency", "intermediate_opponent_compatibility"],
                "feature_opponent_advantage"
            ), 
            node(
                merge_features,
                ["feature_used_pokemon", "feature_type_frequency", "feature_opponent_advantage", "raw_selected_features_name", "parameters"],
                "model_input_feature_merged_data"
            ),

        ]
    )

