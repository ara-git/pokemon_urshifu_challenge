"""Example code for the nodes in the example pipeline. This code is meant
just for illustrating basic Kedro features.

Delete this when you start working on your own Kedro project.
"""

from kedro.pipeline import Pipeline, node

from .node_split_data import split_data
from .node_train import train_GBDT, train_logistic, train_cnn


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                split_data,
                ["model_input_feature_merged_data", "raw_selected_features_name"],
                ["model_input_train_x", "model_input_train_y", "model_input_test_x", "model_input_test_y"]
            ),
            node(
                train_GBDT,
                ["model_input_train_x", "model_input_train_y", "model_input_test_x", "model_input_test_y"],
                "model_output_result_GBDT"
            ),
            node(
                train_logistic,
                ["model_input_train_x", "model_input_train_y", "model_input_test_x", "model_input_test_y"],
                "model_output_result_logistic"
            ),
            node(
                train_cnn,
                ["model_input_train_x", "model_input_train_y", "model_input_test_x", "model_input_test_y"],
                "model_output_result_cnn"
            ),
        ]
    )
