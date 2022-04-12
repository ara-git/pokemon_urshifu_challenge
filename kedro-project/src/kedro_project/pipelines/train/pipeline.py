"""Example code for the nodes in the example pipeline. This code is meant
just for illustrating basic Kedro features.

Delete this when you start working on your own Kedro project.
"""

from kedro.pipeline import Pipeline, node

from .node_split_data import split_data
from .node_train import train_GBDT, train_logistic, train_cnn
from .node_train_gbdt import train_gbdt

def create_pipeline(**kwargs):
    return Pipeline(
        [   node(
                train_gbdt,
                ["model_input_feature_merged_data", "params:gbdt_max_bin", "params:gbdt_num_leaves"],
                outputs=None
            )
        ]
    )
