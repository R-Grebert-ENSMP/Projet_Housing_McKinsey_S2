from kedro.pipeline import node, Pipeline
from immo.pipelines.data_engineering.nodes import (
    sep_voies,
    mask_duplica_vf,
    normalisation,
    normalisation_vf,
    normalisation_cad,
    merger,
    get_square_meter_price,
    corr_type_de_voie_vf,
)




def pipeline_merge_arrond_2014( **kwargs):
    return Pipeline (
    [
        node(func = sep_voies,
            inputs = 'adresses-cadastre-75001',
            outputs = 'cadastre_trie',
            name = 'cadastre_trie'
        ),

        node(func = normalisation_cad,
            inputs = 'cadastre_trie',
            outputs = 'cadastre_normed',
            name = 'cadastre_normed'
        ),

        node(func = mask_duplica_vf,
            inputs = 'valeursfoncieres-2015-01',
            outputs = 'vf_paris_sqm',
            name = 'vf_paris_sqm'
        ),

        node(func=normalisation_vf,
             inputs='vf_paris_sqm',
             outputs='vf_paris_normed',
             name='vf_paris_normed'
             ),

        node(func = merger,
             inputs = ['cadastre_normed', 'vf_paris_normed'],
             outputs = 'master_2014_75001',
             name = 'master_2014-75001'),
        ]
    )

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    