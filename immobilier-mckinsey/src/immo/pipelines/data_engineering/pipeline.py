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
            outputs = 'vf_paris_sqm_15',
            name = 'vf_paris_sqm_15'
        ),

        node(func=normalisation_vf,
             inputs='vf_paris_sqm_15',
             outputs='vf_paris_normed_15',
             name='vf_paris_normed_15'
             ),

        node(func = merger,
             inputs = ['cadastre_normed', 'vf_paris_normed_15'],
             outputs = 'master_2015_75001',
             name = 'master_2015-75001'),

        node(func=mask_duplica_vf,
             inputs='valeursfoncieres-2014-01',
             outputs='vf_paris_sqm_14',
             name='vf_paris_sqm_2'
             ),

        node(func=normalisation_vf,
             inputs='vf_paris_sqm_14',
             outputs='vf_paris_normed_14',
             name='vf_paris_normed_14'
             ),

        node(func=merger,
             inputs=['cadastre_normed', 'vf_paris_normed_14'],
             outputs='master_2014_75001',
             name='master_2014-75001'),

        node(func=mask_duplica_vf,
             inputs='valeursfoncieres-2016-01',
             outputs='vf_paris_sqm_16',
             name='vf_paris_sqm_16'
             ),

        node(func=normalisation_vf,
             inputs='vf_paris_sqm_16',
             outputs='vf_paris_normed_16',
             name='vf_paris_normed_16'
             ),

        node(func=merger,
             inputs=['cadastre_normed', 'vf_paris_normed_16'],
             outputs='master_2016_75001',
             name='master_2016-75001'),

        node(func=mask_duplica_vf,
             inputs='valeursfoncieres-2017-01',
             outputs='vf_paris_sqm_17',
             name='vf_paris_sqm_17'
             ),

        node(func=normalisation_vf,
             inputs='vf_paris_sqm_17',
             outputs='vf_paris_normed_17',
             name='vf_paris_normed_17'
             ),

        node(func=merger,
             inputs=['cadastre_normed', 'vf_paris_normed_17'],
             outputs='master_2017_75001',
             name='master_2017-75001'),

        node(func=mask_duplica_vf,
             inputs='valeursfoncieres-2018-01',
             outputs='vf_paris_sqm_18',
             name='vf_paris_sqm_18'
             ),

        node(func=normalisation_vf,
             inputs='vf_paris_sqm_18',
             outputs='vf_paris_normed_18',
             name='vf_paris_normed_18'
             ),

        node(func=merger,
             inputs=['cadastre_normed', 'vf_paris_normed_18'],
             outputs='master_2018_75001',
             name='master_2018-75001'),
        ]
    )