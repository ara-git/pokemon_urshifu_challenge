"""Example code for the nodes in the example pipeline. This code is meant
just for illustrating basic Kedro features.

Delete this when you start working on your own Kedro project.
"""

from kedro.pipeline import Pipeline, node

from .node_train import train

def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                train,
                ["intermediate_preprocessed_data"],
                ["model_output_weight"]
            ),
        ]
    )
