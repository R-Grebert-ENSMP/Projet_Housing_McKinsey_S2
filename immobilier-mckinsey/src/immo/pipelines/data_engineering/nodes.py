
import jellyfish
import pandas as pd
from pandas.testing import assert_frame_equal
from immo.pipelines.data_engineering.global_variables import parameters
    # Since normalization rules have to be applied to multiple dataframes, you better make them global
    # Careful with column names, they can make you spend hours debugging
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
    for encod_err, encod_corr in parameters["norm_accents"].items():
        str_accents = str_accents.replace(encod_err, encod_corr)
    # Lowercase the string
    str_lower = str_accents.lower()
    # Remove stop_words
    str_stopwords = " ".join(
        [
            word
            for word in str_lower.split(" ")
            if (word not in parameters["stop_words"]) and (len(word) > 0)
        ]
    )
    # Abbreviate common names
    str_abbreviate = str_stopwords
    for long_name, abbr_name in parameters["norm_abbrevations"].items():
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

# ------------------- Merger -------------------#

def merger(clean_cadastre, clean_valeur_fonc, columns_merger = ["No voie","Type de voie","Voie", parameters["vf_price_nominal"], parameters["vf_built_area" ],
parameters["vf_square_meter_price"]], columns_cadastre_compare = [parameters["cad_street_num"],parameters["cad_street_type"],parameters["cad_street_name"]], columns_vf_compare = [parameters["vf_street_num"],parameters["vf_street_type"],parameters["vf_street_name"]]):


    '''
    This fucntion is the final step, it takes the clean table of  cadastre as the scafold, it also needs the name of the columns that need to be compared in both and the list of columns that we want to add to the scafold from valeur fonciere. Then it compares the data and everytime it gets a match, the data from valeur fonciere is added to the scafold.
    Args:
        clean_cadastre (pandas dataframe): the cleaned table of cadastre
        clean_valeur_fonciere (pandas dataframe): the cleaned table of valeur fonciere
        columns_merger (list): list of columns to add to the clean cadastre
        columns_compare (list): list of columns to compare between the two sets
    Returns:
        master_table_f (pandas dataframe): the final master table with both sets merged
    '''


    master_table = clean_cadastre.copy() #Copying of cadastre
    long_columns_merger = len(columns_merger)
    for i in columns_merger:
        master_table[i] = np.NaN

    M1 = np.array(clean_cadastre)
    M2 = np.array(clean_valeur_fonc) # Passing to numpy
    R = np.array(master_table)
    columns_clean_cadastre = list(clean_cadastre.columns)
    columns_clean_valeur_fonc = list(clean_valeur_fonc.columns)
    columns_master_table = list(master_table.columns)

    indexem_columns_clean_valeur_fonc = [columns_clean_valeur_fonc.index(i) for i in columns_merger] # Indexes of the columns in valeur_fonciere to merge

    indexem_columns_master_table = [columns_master_table.index(i) for i in columns_merger] # Indexes of the columns in master_table to merge

    #Those list are necessary to work with numpy instead of pandas
    indexec_columns_clean_cadastre = [columns_clean_cadastre.index(i) for i in columns_cadastre_compare] # Indexes of the columns in cadastre that we have to compare

    indexec_columns_clean_valeur_fonc = [columns_clean_valeur_fonc.index(i) for i in columns_vf_compare] # Indexes of the columns in valeur_fonciere that we have to compare

    a = len(M1[:,0])
    b = len(M1[:,0])


#Since we are basing our comparison on the number, street type and street, I created a tuple with those 3 infos in it, this tuple needs to be modified if we are to compare other informations between the two sets

    for i in range (a):
        (Num1, Type1, Voie1) = (M1[i, p] for p in indexec_columns_clean_cadastre)

        for j in range (b):
            (Num2, Type2, Voie2) = (M2[j, p] for p in indexec_columns_clean_cadastre)

            if compare(Num1, Type1, Voie1, Num2, Type2, Voie2):

                for k in range (long_columns_merger):
                    R[i, indexem_columns_master_table[k]] = M2[j, indexem_columns_clean_valeur_fonc[k]]

    master_table_f = pd.DataFrame(R)
    master_table_f.columns = master_table.columns

    return master_table_f

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
    cadastre_df[parameters["cad_street_type"]] = cadastre_df[parameters["cad_street_full"]].apply(
        lambda x: x.split(" ")[0]
    )
    cadastre_df[parameters["cad_street_name"]] = cadastre_df[parameters["cad_street_full"]].apply(
        lambda x: " ".join(x.split(" ")[1:])
    )
    return cadastre_df.drop(parameters["cad_street_full"], axis=1)


def corr_type_de_voie_vf(valeur_fonc_df):
    """
    Corrects the vf_street_type column in the "valeur foncière" table, for future comparison with the "cadastre table".
    Corrections are made according to the norm_street_types dictionary in defined in global variables.

    Args:
        valeur_fonc_df (pandas dataframe): a dataframe with a street_type column to be standardized to the values in cadastre

    Returns:
        pandas dataframe: the same dataframe, with standardized values in the street_type column
    """
    valeur_fonc_df[parameters["vf_street_type"]] = valeur_fonc_df[parameters["vf_street_type"]].apply(
        lambda x: parameters["norm_street_types[x]"] if x in parameters["norm_street_types"].keys() else x
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
    Corrects the vf_square_meter_price column in the "valeur foncière" table, as vf_price_nominal divided by vf_built_area. Returns "undefined" where area = 0.

    Args:
        valeur_fonc_df (pandas dataframe): a dataframe with vf_price_nominal and vf_built_area columns.

    Returns:
        pandas dataframe: the same dataframe, with the new vf_square_meter_price column.
    """
    def exception(price,area) :
        if area == 0 :
            return "undefined"
        else :
            return price/area

    valeur_fonc_df[parameters["vf_square_meter_price"]] = valeur_fonction_df.groupby([valeur_fonc_df[parameters["vf_price_nominal"]] , valeur_fonc_df[parameters["vf_built_area"]]]).apply(exception, axis = 1)
    return valeur_fonc_de


#------------------------------------------------------------- not cleaned

##Nous avons finalement décidé de ne pas découper cadastre_75 en arrondissement

# #----functions and parameters for cond_filtering_cadastre
# def first_digits(number):
#     if str(number)[:2]!='na':
#         return int(str(number)[:2])
#     else:
#         return 0
#
# CODE_POSTAL_CADASTRE = 'code_postal'
# CODE_POSTAL_VF = 'code_postal'
# ARROND=750
#
# def cond_filtering_cadastre(cadastre_df, code_postal = CODE_POSTAL_CADASTRE , arrond = ARROND):
#     """
#     Selects the part of the "cadastre_df" corresponding to the appropriate postal code
#
#     """
#     return cadastre_df[cadastre_df[code_postal].apply(first_digits) == arrond]
# #-------








