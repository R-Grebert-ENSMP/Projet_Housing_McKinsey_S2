from kedro.pipeline import node, Pipeline
from immo.pipelines.data_engineering.nodes import (
    sep_voies,
    cond,
    cond_filtering_cadastre,
    duplica,
    corr_type_de_voie,
)


def pipeline_merge_arrond_2014( **kwargs):
    return Pipeline (
    [   
        node(func = sep_voies,
            inputs = ['adresses-cadastre-75'],
            outputs = 'cadastre_trie',
            name = 'cadastre_trie'
        ),
        
        node(func = cond_filtering_cadastre,
           inputs = 'cadastre_trie',
            outputs = 'cadastre_i',
            name = 'cadastre_i'
        ),

        ]
    )
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    