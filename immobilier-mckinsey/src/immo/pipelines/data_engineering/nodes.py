
import jellyfish
import pandas as pd
from pandas.testing import assert_frame_equal
from global_variables import (
    # Since normalization rules have to be applied to multiple dataframes, you better make them global
    norm_street_types,
    norm_accents,
    norm_abbrevations,
    stop_words,
    # Careful with column names, they can make you spend hours debugging
    vf_street_type,
    vf_price_nominal,
    vf_built_area,
    vf_square_meter_price,
    cad_street_full,
    cad_street_type,
    cad_street_name,
)

import json
import numpy as np
import math
import matplotlib.pyplot as plt
import folium
from shapely.geometry import Point, Polygon
import geopandas




# ------------------- Merging Functions ------------------- #

#-------------------------------------------------------cleaned

def normalisation(str_err):
    """
    Function to normalize a string through four steps :
    - replacing errors related to accents encoding
    - lowercasing
    - stop words removal
    - normalizing common names (place, general, ...) into abbreviations
    Normalization rules are imported from global variables.py

    Args:
        str_err (string): the string to normalize

    Returns:
        string: the normalized string
    """
    # Replace accents related errors
    str_accents = str_err
    for encod_err, encod_corr in norm_accents.items():
        str_accents = str_accents.replace(encod_err, encod_corr)
    # Lowercase the string
    str_lower = str_accents.lower()
    # Remove stop_words
    str_stopwords = " ".join(
        [
            word
            for word in str_lower.split(" ")
            if (word not in stop_words) and (len(word) > 0)
        ]
    )
    # Abbreviate common names
    str_abbreviate = str_stopwords
    for long_name, abbr_name in norm_abbrevations.items():
        str_abbreviate = str_abbreviate.replace(long_name, abbr_name)
    return str_abbreviate


def compare(
    ref_address_number,
    ref_address_type,
    ref_address_street,
    comp_address_number,
    comp_address_type,
    comp_address_street,
    distance_threshold=0.9,
):
    """
    Computes the Jaro Distance (https://rosettacode.org/wiki/Jaro_distance) on two normalized strings.
    The normalization process is developed in the normalisation function.
    Requires jellyfish version xx.yy.

    Args:
        ref_address_number (string): the number of the address to compare with
        ref_address_type (string): the type of the address to compare with
        ref_address_street (string): the street of the address to compare with
        comp_address_number (string): the number of the address to be compared
        comp_address_type (string): the type of the address to be compared
        comp_address_street (string): the street of the address to be compared
        distance_threshold (float): the [0, 1] threshold on the Jaro distance that returns the boolean

    Returns:
        boolean: did the Jaro distance match the ref address and comp address ?
    """
    # If the type and number of the addresses are the same,
    match_condition = ref_address_number == comp_address_number
    match_condition &= ref_address_type == comp_address_type
    # and the distance is upper than the threshold (0: no similarity, 1: perfect match),
    ref_norm = normalisation(" " + ref_address_street)
    comp_norm = normalisation(" " + comp_address_street)
    match_condition &= jellyfish.jaro_distance(ref_norm, comp_norm) > distance_threshold
    # then the addresses are the same
    if match_condition:
        return True
    else:
        return False


# ------------------- Cleaning Functions ------------------- #




def sep_voies(cadastre_df):
    """
    Splits the cad_street_full column in the cadastre into cad_street_type and cad_street name,
    to match the format in the "valeurs foncieres" table.

    Args:
        cadastre_df (pandas dataframe): the cadastre table

    Returns:
        pandas dataframe: the cadastre table, with the cad_street_full column,
        splitted into the cad_street_type and cad_street_name columns.
    """
    # The pd.DataFrame.apply() method is the best to apply any type of function
    # It prevents from looping on pd df, which is very costly
    cadastre_df[cad_street_type] = cadastre_df[cad_street_full].apply(
        lambda x: x.split(" ")[0]
    )
    cadastre_df[cad_street_name] = cadastre_df[cad_street_full].apply(
        lambda x: " ".join(x.split(" ")[1:])
    )
    return cadastre_df.drop(cad_street_full, axis=1)


def corr_type_de_voie_vf(valeur_fonc_df):
    """
    Corrects the vf_street_type column in the "valeur foncière" table, for future comparison with the "cadastre table".
    Corrections are made according to the norm_street_types dictionary in defined in global variables.

    Args:
        valeur_fonc_df (pandas dataframe): a dataframe with a street_type column to be standardized to the values in cadastre

    Returns:
        pandas dataframe: the same dataframe, with standardized values in the street_type column
    """
    valeur_fonc_df[vf_street_type] = valeur_fonc_df[vf_street_type].apply(
        lambda x: norm_street_types[x] if x in norm_street_types.keys() else x
    )
    return valeur_fonc_df


def mask_duplica_vf(df_vf):

    """

    This function selects the Paris lines in the "valeur fonciere" dataframe

    It then groups the parcels sold together (same adress) in a single surface and deletes the useless lines in order to only have one line for each individual parcel under the same adress


    """
    df_paris = pd.DataFrame(columns = df_vf.columns)
    for i in range (75001, 75021):
        df_paris = master.append(cond(df_vf, 'Code postal', i))

    master = df_paris
    length_paris = len(df_paris.index)
    master.index = [i for i in range (n)]
    C_surface = np.array(master['Surface reelle bati'])
    i = 0
    while i < n-1:
        k = 1
        surface_i = master.loc[i]['Surface reelle bati']
        if master.duplicated(['Valeur fonciere', 'Date mutation', 'Section'])[i]:
            while master.loc[i]['Section'] == master.loc[i+k]['Section']:
                surface_i += master.loc[i+k]['Surface reelle bati']
                k += 1
            C_surface[i] = surface_i
        i += k
    del master['Surface reelle bati']
    master.insert(38,'Surface reelle bati' ,C_surface)
    return master.drop_duplicates(['Date mutation', 'Valeur fonciere', 'Section'], keep='first')


def get_square_meter_price(valeur_fonc_df):
    """
    Corrects the vf_square_meter_price column in the "valeur foncière" table, as vf_price_nominal divided by vf_built_area.

    Args:
        valeur_fonc_df (pandas dataframe): a dataframe with vf_price_nominal and vf_built_area columns.

    Returns:
        pandas dataframe: the same dataframe, with the new vf_square_meter_price column.
    """
    valeur_fonc_df[vf_square_meter_price] = (
        valeur_fonc_df[vf_price_nominal] / valeur_fonc_df[vf_built_area]
    ).round()
    # TO DO : catch the surface == 0 exception
    return valeur_fonc_df


#------------------------------------------------------------- not cleaned




#----functions and parameters for cond_filtering_cadastre
def first_digits(number):
    if str(number)[:2]!='na':
        return int(str(number)[:2])
    else:
        return 0

CODE_POSTAL_CADASTRE = 'code_postal'
CODE_POSTAL_VF = 'code_postal'
ARROND=750

def cond_filtering_cadastre(cadastre_df, code_postal = CODE_POSTAL_CADASTRE , arrond = ARROND):
    """
    Selects the part of the "cadastre_df" corresponding to the appropriate postal code

    """
    return cadastre_df[cadastre_df[code_postal].apply(first_digits) == arrond]
#-------








