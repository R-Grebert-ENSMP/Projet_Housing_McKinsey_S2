from kedro.pipeline import node, Pipeline
from immo.pipelines.data_engineering.nodes import (
    sep_voies,
    cond,
    duplica,
    corr_type_de_voie,
)

CODE_POSTAL_CADASTRE = 'code_postal'
CODE_POSTAL_VF = 'code_postal'
ARRONDI=750

def pipeline_merge_arrond_2014( **kwargs):
    return Pipeline (
    [   
        node(func = sep_voies,
            inputs = ['adresses-cadastre-75'],
            outputs = 'cadastre_trié',
            name = 'cadastre_trié',
        ),
        
        node(func = cond,
            inputs = ['cadastre_trié', 'CODE_POSTAL_CADASTRE', 'ARRONDI'],
            outputs = 'cadastre_i',
            name = 'cadastre_i',
        ),
        
        node(func = cond,
            inputs = ['valeursfonciere-2014', 'CODE_POSTAL_VF','ARRONDI'],
            outputs = 'master_2014i1_nt',#nt pour non triée
            name = 'vf_2014_i_nt',
        ),
        ]
    )
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    