"""Construction of the master pipeline.
"""

from typing import Dict
from kedro.pipeline import Pipeline

from immo.pipelines.data_engineering import pipeline as de

def create_pipelines(**kwargs) -> Dict[str, Pipeline]:
    de_pipeline = de.pipeline_merge_arrond_1()

    return {
        "de": de_pipeline,
        "__default__": de_pipeline,
    }