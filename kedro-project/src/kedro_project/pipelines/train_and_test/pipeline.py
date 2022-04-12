"""Example code for the nodes in the example pipeline. This code is meant
just for illustrating basic Kedro features.

Delete this when you start working on your own Kedro project.
"""

from kedro.pipeline import Pipeline, node

from .node_train_gbdt import train_gbdt
from .node_train_cnn import train_cnn
from .node_train_logistic import train_logistic
from .node_merge_result import merge_result

def create_pipeline(**kwargs):
    return Pipeline(
        [   node(
                train_gbdt,
                ["model_input_feature_merged_data", "params:gbdt_max_bin", "params:gbdt_num_leaves"],
                outputs= ["model_output_result_gbdt", "model_output_importance_gbdt"]
                ),
            node(
                train_cnn,
                ["model_input_feature_merged_data", "params:cnn_hidden_node_num", "params:cnn_epoch_num", "params:cnn_batch_size"],
                outputs="model_output_result_cnn"
            ),
            node(
                train_logistic,
                "model_input_feature_merged_data",
                outputs="model_output_result_logistic"
            ),
            node(
                merge_result,
                ["model_output_result_gbdt", "model_output_result_cnn", "model_output_result_logistic"],
                outputs="model_output_merged_result"
            )
        ]
    )
