from kedro.pipeline import node, Pipeline
from immo.pipelines.data_engineering.nodes import (
    sep_voies,
    mask_duplica_vf,
    merger,
    normalisation,
    get_square_meter_price,
    corr_type_de_voie_vf,
)
from immo.pipelines.data_engineering.global_variables import parameters


def pipeline_merge_arrond_2014( **kwargs):
    return Pipeline (
    [
        node(func = sep_voies,
            inputs = ['adresses-cadastre-75'],
            outputs = 'cadastre_trie',
            name = 'cadastre_trie'
        ),

        node(func = normalisation,
            inputs = 'cadastre_trie',
            outputs = 'cadastre_normed',
            name = 'cadastre_normed'
        ),

        node(func = mask_duplica_vf,
            inputs = 'valeursfoncieres-2014',
            outputs = 'vf_paris_sqm',
            name = 'vf_paris_sqm'
        ),

        node(func=normalisation,
             inputs='vf_paris',
             outputs='vf_paris_normed',
             name='vf_paris_normed'
             ),

        node(func = merger,
             inputs = ['cadastre_normed', 'vf_paris_normed'],
             outputs = 'master_2014',
             name = 'master_2014'),
        ]
    )

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    