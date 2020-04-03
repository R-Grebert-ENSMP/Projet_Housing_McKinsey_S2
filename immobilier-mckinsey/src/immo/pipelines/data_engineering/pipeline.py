def create_pipeline(**kwargs):
    return Pipeline (
    [
        node(func = selection,
            inputs = ['valeurs-foncieres-2014', "Lat", "Long"]
            outputs = 'df_master_2',
            name = 'df_master_2',
        )
        
        node(func = drop_duplica,
            inputs = ['df_master_2', 'Lat', 'Long']
            outputs = 'df_coord',
            name = 'df_coord',
        )
        
        node(func = geo,
            inputs = 'df_coord',
            outputs = 'df_geo',
            name = 'df_geo',
        )
        
        node(func = merger,
            inputs = ['df_geo', 'EMPRISE_BATI_PARIS', 'left']
            outputs = 'corres_table_coord_apur',
            name = 'corres_table_coord_apur',
        )
        
        node(func = merger,
            inputs = ['valeurs-foncieres-2014', 'corres_table_coord_apur', 'left', ['Lat', 'Long']]
            outputs = 'df_master_3',
            name = 'df_master_3',
        )

    ]
    