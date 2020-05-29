import jellyfish
import pandas as pd
from immo.pipelines.data_engineering.global_variables import parameters
import numpy as np
import math
import matplotlib.pyplot as plt
import folium
from shapely.geometry import Point, Polygon
import geopandas




# ------------------- Merging Functions ------------------- #

#-------------------------------------------------------cleaned

def normalisation (str_err):
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


def normalisation_vf (valeur_fonciere):
    vf_norm = valeur_fonciere.copy()
    vf_norm[parameters["vf_street_name"]] = vf_norm[parameters["vf_street_name"]].apply(normalisation)
    vf_norm[parameters["vf_street_type"]] = vf_norm[parameters["vf_street_type"]].apply(normalisation)
    return vf_norm


def normalisation_cad (cadastre):
    cadastre_norm = cadastre.copy()
    cadastre_norm[parameters["cad_street_name"]] = cadastre_norm[parameters["cad_street_name"]].apply(normalisation)
    cadastre_norm[parameters["cad_street_type"]] = cadastre_norm[parameters["cad_street_type"]].apply(normalisation)
    return cadastre_norm


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
#Il faudra rajouter , parameters["vf_square_meter_price"]
def merger(
        clean_cadastre,
        clean_valeur_fonc,
        columns_merger = [parameters["vf_price_nominal"], parameters["vf_built_area"]],
        columns_cadastre_compare = [parameters["cad_street_num"], parameters["cad_street_type"], parameters["cad_street_name"]],
        columns_vf_compare = [parameters["vf_street_num"], parameters["vf_street_type"], parameters["vf_street_name"]]
        ):

    '''
    This fucntion is the final step, it takes the clean table of  cadastre as the scafold, it also needs the name of the
    columns that need to be compared in both and the list of columns that we want to add to the scafold from valeur fonciere.
    Then it compares the data and everytime it gets a match, the data from valeur fonciere is added to the scafold.
    Args:
        clean_cadastre (pandas dataframe): the cleaned table of cadastre
        clean_valeur_fonciere (pandas dataframe): the cleaned table of valeur fonciere
        columns_merger (list): list of columns to add to clean cadastre
        columns_cadastre_compare (list): list of columns in cadastre to compare with valeur fonciere
        columns_vf_compare (list): list of columns in valeur fonciere to compare with cadastre

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
    b = len(M2[:,0])


#Since we are basing our comparison on the number, street type and street, I created a tuple with those 3 infos in it, this tuple needs to be modified if we are to compare other informations between the two sets

    for i in range (a):
        (Num1, Type1, Voie1) = (M1[i, p] for p in indexec_columns_clean_cadastre)

        for j in range (b):
            (Num2, Type2, Voie2) = (M2[j, p] for p in indexec_columns_clean_valeur_fonc)

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
    cadastre_df.loc[:,parameters["cad_street_type"]] = cadastre_df.loc[:,parameters["cad_street_full"]].apply(
        lambda x: x.split(" ")[0]
    )
    cadastre_df.loc[:,parameters["cad_street_name"]] = cadastre_df.loc[:,parameters["cad_street_full"]].apply(
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

def mask_vf(valeur_fonciere):
    '''
    This function applies a mask to the dataset in order to extract only the values concerning paris in valeur fonciere

    Args: valeur fonciere (pandas dataframe)

    Returns: pandas dataframe: only parisian datas
    '''

    valeur_fonciere_paris = pd.DataFrame(columns = valeur_fonciere.columns)
    for i in range (75001, 75021):
        valeur_fonciere_paris = pd.concat([valeur_fonciere_paris, cond(valeur_fonciere, i)])
    return df_paris

def cond(df, arrond):
    '''
    This is a small function just to apply the condition on the postal code

    Args:
        df (dataframe),
        arrond(int): the value of the borough

    Returns:
        dataframe with only the selected borough
    '''
    return df[df['Code postal'] == arrond]

def mask_duplica_vf(df_paris):
    '''
    This function takes a valeur_fonciere and it goes looking for every identical lot. Because in vf a real estate lot
    are devided in multiple lines and to execute our programs we want only one line with one price and one area. Therefore
    when it finds 2+ lines with the same price, date and section number it adds the area of the lines under to the 1rst one
    then deletes them ar the very end of the program.
    To avoid comparing every line I only compare the one where we know there is a duplicate in the DataFrame.

    Args: df_paris (Panda DataFrame only concerning paris)

    Returns: dataframe
    '''
    master = df_paris.copy()
    length_paris = len(df_paris.index)
    master.index = [i for i in range (length_paris)] #Re-indexing the lines from 0 to the total number of lines
    C_surface = np.array(master.loc[:,parameters["vf_built_area"]]) #Creating a new column where the new areas are going to be in
    i = 0
    while i < length_paris-1:
        k = 1
        surface_i = master.loc[i][parameters["vf_built_area"]]
        if master.duplicated([parameters["vf_price_nominal"], parameters["vf_mutation_date"], parameters["vf_built_area"]])[i]:
            #This is to compare only lines where we know a duplicate only on 'Valeur fonciere', 'Date mutation', 'Section' exists

            while master.loc[i][parameters["vf_built_area"]] == master.loc[i+k][parameters["vf_built_area"]]:#If a duplicate exists it is necessarily right under
                #So we just have to compare a key we know is in common here I chose Section
                surface_i += master.loc[i+k][parameters["vf_built_area"]]
                k += 1
            C_surface[i] = surface_i
        i += k
    del master[parameters["vf_built_area"]]
    master.insert(38,parameters["vf_built_area"], C_surface)
    #we delete and replace the 'area colmun' by the new one (38 because that is the index of the column area in valeur fonciere)
    master_f = master.drop_duplicates([parameters["vf_mutation_date"], parameters["vf_price_nominal"],
                                      parameters["vf_built_area"]])
    #Then we delete all the duplicates we compared before
    return(master_f) #We combine get square meter et mask


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

#------------------------------------------------------------- not cleaned

##Nous avons finalement décidé de ne pas découper cadastre_75 en arrondissement

#functions and parameters for cond_filtering_cadastre
#def first_digits(number):
#     if str(number)[:2]!='na':
#         return int(str(number)[:2])
#     else:
#        return 0

#CODE_POSTAL_CADASTRE = 'code_postal'
#CODE_POSTAL_VF = 'code_postal'
#ARROND=750

#def cond_filtering_cadastre(cadastre_df, code_postal = CODE_POSTAL_CADASTRE , arrond = ARROND):
#    """
#     Selects the part of the "cadastre_df" corresponding to the appropriate postal code
#
#     """
#     return cadastre_df[cadastre_df[code_postal].apply(first_digits) == arrond]





