import pandas as pd
import numpy as np
parameters = {
# Column Names
# Valeurs Foncieres table
"vf_street_num" : "No voie",
"vf_street_name" : "Voie",
"vf_street_type" : "Type de voie",
"vf_price_nominal" : "Valeur fonciere",
"vf_built_area" : "Surface reelle bati",
}
def get_square_meter_price(valeur_fonc_df):
    """
    Corrects the vf_square_meter_price column in the "valeur foncière" table, as vf_price_nominal divided by vf_built_area.
    Args:
        valeur_fonc_df (pandas dataframe): a dataframe with vf_price_nominal and vf_built_area columns.
    Returns:
        pandas dataframe: the same dataframe, with the new vf_square_meter_price column.
    """
    master = valeur_fonc_df.copy()
    master['vf_square_meter_price'] = np.where(master[parameters["vf_built_area"]] == np.nan,
                                                master[parameters["vf_price_nominal"]],
                                               master[parameters["vf_price_nominal"]]/master[parameters["vf_built_area"]])

    return master

master1 = pd.DataFrame({'Surface reelle bati': [30 , np.NaN, 50], 'Valeur fonciere': [1000, 2000, 3000]})
print(get_square_meter_price(master1))