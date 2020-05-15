from kedro.pipeline import node, Pipeline
from immo.pipelines.data_engineering.nodes import (
    sep_voies,
    mask_duplica_vf,
    normalisation,
    merger,
    get_square_meter_price,
    corr_type_de_voie_vf,
    create_master_table,

)




def pipeline_merge_arrond( **kwargs):
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
        #for vf_2014

        node(func = mask_duplica_vf,
            inputs = 'valeursfoncieres-2014',
            outputs = 'vf_paris_sqm_2014',
            name = 'vf_paris_sqm_2014'
        ),

        node(func=normalisation,
             inputs='vf_paris_sqm',
             outputs='vf_paris_normed_2014',
             name='vf_paris_normed_2014'
        ),

        node(func = merger,
             inputs = ['cadastre_normed', 'vf_paris_normed_2014'],
             outputs = 'master_2014',
             name = 'master_2014'
        ),
        #for vf_2015

        node(func = mask_duplica_vf,
            inputs = 'valeursfoncieres-2015',
            outputs = 'vf_paris_sqm_2015',
            name = 'vf_paris_sqm_2015'
        ),

        node(func=normalisation,
             inputs='vf_paris_sqm_2015',
             outputs='vf_paris_normed_2015',
             name='vf_paris_normed_2015'
             ),

        node(func = merger,
             inputs = ['cadastre_normed', 'vf_paris_normed_2015'],
             outputs = 'master_2015',
             name = 'master_2015'
        ),
        #for vf_2016

        node(func = mask_duplica_vf,
            inputs = 'valeursfoncieres-2016',
            outputs = 'vf_paris_sqm_2016',
            name = 'vf_paris_sqm_2016'
        ),

        node(func=normalisation,
             inputs='vf_paris_sqm_2016',
             outputs='vf_paris_normed_2016',
             name='vf_paris_normed_2016'
             ),

        node(func = merger,
             inputs = ['cadastre_normed', 'vf_paris_normed_2016'],
             outputs = 'master_2016',
             name = 'master_2016'
        ),
        #for vf_2017

        node(func = mask_duplica_vf,
            inputs = 'valeursfoncieres-2017',
            outputs = 'vf_paris_sqm_2017',
            name = 'vf_paris_sqm_2017'
        ),

        node(func=normalisation,
             inputs='vf_paris_sqm_2017',
             outputs='vf_paris_normed_2017',
             name='vf_paris_normed_2017'
             ),

        node(func = merger,
             inputs = ['cadastre_normed', 'vf_paris_normed_2017'],
             outputs = 'master_2017',
             name = 'master_2017'
        ),
        #for vf_2018

        node(func = mask_duplica_vf,
            inputs = 'valeursfoncieres-2018',
            outputs = 'vf_paris_sqm_2018',
            name = 'vf_paris_sqm_2018'
        ),

        node(func=normalisation,
             inputs='vf_paris_sqm_2018',
             outputs='vf_paris_normed_2018',
             name='vf_paris_normed_2018'
             ),

        node(func = merger,
             inputs = ['cadastre_normed', 'vf_paris_normed_2018'],
             outputs = 'master_2018',
             name = 'master_2018'),
        #Creating master table

        node(func = create_master_table,
            inputs = ['master_2014','master_2015','master_2016','master_2017','master_2018'],
            outputs = 'master_table',
            name = 'master_table'),
        ]
    )













