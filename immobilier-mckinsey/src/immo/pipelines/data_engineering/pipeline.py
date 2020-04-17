from kedro.pipeline import node, Pipeline
from immo.pipelines.data_engineering.nodes import (
    merger,
    selection,
    drop_duplica,
    geo,
)


def pipeline_merge_arrond_2014(i, **kwargs):
    return Pipeline (
    [   
        node(func = sep_voies,
            inputs = ['adresses-cadastre-75'],
            outputs = 'cadastre_trié',
            name = 'cadastre_trié',
        ),
        
        node(func = cond,
            inputs = ['cadastre_trié', 'code_postal', 750i],
            outputs = 'cadastre_i',
            name = 'cadastre_i',
        ),
        
        node(func = cond,
            inputs = ['valeursfonciere-2014', 'Code postal', 750i],
            outputs = 'master_2014i1_nt',#nt pour non triée
            name = 'vf_2014_i_nt',
        ),
        
        node(func = duplica,
            inputs = ['master_2014_i_nt'],
            outputs = 'master_2014_i_nc', #nc pour on corrigé
            name = 'vf_2014_i_nc',
        ),
        
        node(func = corr_type_de_voie,
            inputs = ['master_2014_i_nc'],
            outputs = 'master_2014_i_n', 
            name = 'vf_2014_i_n',
        ),
        
        node(func = corr_type_de_voie,
            inputs = ['master_2014_i_n'],
            outputs = 'master_2014_i', 
            name = 'vf_2014_i',
        ),
        
        #On a cadastre du ième arrondissement avec les bonnes colonnes et valeurs foncières 2014 du ième arrondissement avec le nom des voies corrigées
        
    ]
    )
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    