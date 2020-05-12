from kedro.pipeline import node, Pipeline
from immo.pipelines.data_engineering.nodes import (
    sep_voies,
    mask_duplica_vf,
    cond_filtering_cadastre,
    normalisation,
    first_digits,
    get_square_meter_price,
    corr_type_de_voie_vf,
)
from immo.pipelines.data_engineering.nodes.global_variables


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

        node(func = normalisation,
           inputs = 'cadastre_i',
            outputs = 'cadastre_i_normed',
            name = 'cadastre_i_normed'
        ),

        node(func = mask_duplica_vf,
           inputs = 'valeursfoncieres-2014',
            outputs = 'vf_paris',
            name = 'vf_paris'
        ),

        node(func = get_square_meter_price,
           inputs = 'vf_paris',
            outputs = 'vf_paris_sqm',
            name = 'vf_paris_sqm'
        ),

        node(func = corr_type_de_voie_vf,
           inputs = 'vf_paris_sqm',
            outputs = 'vf_paris_corr',
            name = 'vf_paris_corr'
        ),


        ]
    )














