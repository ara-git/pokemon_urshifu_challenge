"""Project pipelines."""
import os
from typing import Dict

from kedro.pipeline import Pipeline
from kedro_project.pipelines import get_data
from kedro_project.pipelines import preprocess

def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """
    get_data_pipeline = get_data.create_pipeline()
    preprocess_pipeline = preprocess.create_pipeline()

    if os.environ.get("get_data") == "True":
        # データのインストールから行う場合
        return {"get_data": get_data_pipeline, "preprocess": preprocess_pipeline, "__default__": get_data_pipeline + preprocess_pipeline}
    else:
        # データの前処理から行う場合
        return {"preprocess": preprocess_pipeline, "__default__": preprocess_pipeline}