"""Construction of the master pipeline.
"""

from typing import Dict
from kedro.pipeline import Pipeline
from immo.pipelines.data_engineering.nodes import (
    merger,
    selection,
    drop_duplica,
    geo,
)
from immo.pipelines.data_engineering import pipeline as de

def create_pipelines(**kwargs) -> Dict[str, Pipeline]:

    return {
        "__default__": Pipeline([])
    }

