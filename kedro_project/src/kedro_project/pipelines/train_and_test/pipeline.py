"""Example code for the nodes in the example pipeline. This code is meant
just for illustrating basic Kedro features.

Delete this when you start working on your own Kedro project.
"""
import os
from kedro.pipeline import Pipeline, node

from .node_split_data import split_data
from .node_train_gbdt import train_gbdt
from .node_train_cnn import train_cnn
from .node_train_logistic import train_logistic
from .node_calc_score import calc_score

from .node_train_gbdt_use_full_data import train_gbdt_full_data
from .node_train_cnn_use_full_data import train_cnn_full_data
from .node_train_logistic_use_full_data import train_logistic_full_data

def create_pipeline(**kwargs):
    if os.environ.get("save_weight") == "True":
        """
        streamlitアプリ用の重みを計算する。
        環境変数 "save_weight"がTrueの時のみ実行する。

        基本的にすべてのデータを使う。
        """
        return Pipeline(
            [   
                node(
                    train_gbdt_full_data,
                    ["model_input_feature_merged_data", "params:gbdt_max_bin", "params:gbdt_num_leaves"],
                    outputs = None
                ),
                node(
                    train_cnn_full_data,
                    ["model_input_feature_merged_data", "params:cnn_hidden_node_num", "params:cnn_epoch_num", "params:cnn_batch_size"],
                    outputs = None
                ),
                node(
                    train_logistic_full_data,
                    "model_input_feature_merged_data",
                    outputs = None
                ),
            ]
            )
    else:
        return Pipeline(
        [   
            node(
                split_data,
                "model_input_feature_merged_data",
                outputs = ["model_input_train_x", "model_input_train_y", "model_input_test_x", "model_input_test_y"],
                ),
            node(
                train_gbdt,
                ["model_input_train_x", "model_input_train_y", "model_input_test_x", "params:gbdt_max_bin", "params:gbdt_num_leaves"],
                outputs= ["model_output_prediction_gbdt", "model_output_importance_gbdt"]
                ),
            node(
                train_cnn,
                ["model_input_train_x", "model_input_train_y", "model_input_test_x", "params:cnn_hidden_node_num", "params:cnn_epoch_num", "params:cnn_batch_size"],
                outputs="model_output_prediction_cnn"
            ),
            node(
                train_logistic,
                ["model_input_train_x", "model_input_train_y", "model_input_test_x"],
                outputs="model_output_prediction_logistic"
            ),
            node(
                calc_score,
                ["model_input_test_y", "model_output_prediction_gbdt", "model_output_prediction_cnn", "model_output_prediction_logistic"],
                outputs="model_output_prediction_result"
            ),
        ]
    )