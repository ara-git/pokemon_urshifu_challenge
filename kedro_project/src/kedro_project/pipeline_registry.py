"""Project pipelines."""
import os
from typing import Dict

from kedro.pipeline import Pipeline
from kedro_project.pipelines import get_data_PocketFunction
from kedro_project.pipelines import preprocess
from kedro_project.pipelines import train_and_test
from kedro_project.pipelines import get_data_ShowDown

def register_pipelines() -> Dict[str, Pipeline]:
    get_data_pf_pipeline = get_data_PocketFunction.create_pipeline()
    get_data_sd_pipeline = get_data_ShowDown.create_pipeline()
    preprocess_pipeline = preprocess.create_pipeline()
    train_and_test_pipeline= train_and_test.create_pipeline()
    
    return_dict = {"preprocess": preprocess_pipeline, "train_and_test": train_and_test_pipeline, "__default__": preprocess_pipeline + train_and_test_pipeline}

    if os.environ.get("get_data_pf") == "True":
        # ぽけっとふぁんくしょんからのデータ読み込みから行う場合、パイプラインを追加する
        return_dict["get_data_pf"] = get_data_pf_pipeline
        return_dict["__default__"] = get_data_pf_pipeline + return_dict["__default__"]

    if os.environ.get("get_data_sd_get_url") == "True" or os.environ.get("get_data_sd_download_html") == "True" or os.environ.get("get_data_sd_read_html") == "True":
        # ShowDownからのデータ読み込みから行う場合、パイプラインを追加する
        return_dict["get_data"] = get_data_sd_pipeline
        return_dict["__default__"] = get_data_sd_pipeline + return_dict["__default__"]

    print(return_dict)
    return return_dict
