from kedro.pipeline import node, Pipeline
from immo.pipelines.data_engineering.nodes import (
    merger,
    selection,
    drop_duplica,
    geo,
)


def create_pipeline(**kwargs):
    return Pipeline (
    [
        node(func = selection,
            inputs = ['adresses-cadastre-75', "long", "lat"],
            outputs = 'df_master_2',
            name = 'scafolding',
        ),
        
    ]
    )