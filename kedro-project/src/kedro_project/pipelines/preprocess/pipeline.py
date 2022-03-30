"""Example code for the nodes in the example pipeline. This code is meant
just for illustrating basic Kedro features.

Delete this when you start working on your own Kedro project.
"""

from kedro.pipeline import Pipeline, node

from .node_preprocess import preprocess

def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                preprocess,
                ["raw_dark_urshifu_data", "raw_water_urshifu_data"],
                ["intermediate_data"]
            ),
        ]
    )
