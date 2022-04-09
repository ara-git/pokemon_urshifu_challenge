"""Project pipelines."""
import os
from typing import Dict

from kedro.pipeline import Pipeline
from kedro_project.pipelines import get_data_PocketFunction
from kedro_project.pipelines import preprocess
from kedro_project.pipelines import train

def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """
    get_data_pipeline = get_data_PocketFunction.create_pipeline()
    preprocess_pipeline = preprocess.create_pipeline()
    train_pipeline= train.create_pipeline()
    
    return_dict = {"preprocess": preprocess_pipeline, "train": train_pipeline, "__default__": preprocess_pipeline + train_pipeline}

    if os.environ.get("get_data_pf") == "True":
        # ぽけっとふぁんくしょんからのデータ読み込みから行う場合、パイプラインを追加する
        return_dict["get_data"] = get_data_pipeline
        return_dict["__default__"] = get_data_pipeline + return_dict["__default__"]

    return return_dict
