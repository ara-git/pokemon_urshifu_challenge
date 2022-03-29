"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline
from kedro_project.pipelines import get_data

def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """
    get_data_pipeline = get_data.create_pipeline()
    
    return {"get_data": get_data_pipeline, "__default__": get_data_pipeline}