"""
Basically, this script gathers the functions from the following scripts :
    - compareadresse.py
    - corr_type_voie_VF.py
    - normalisation_et_stop_words.py
    - rajout_prix_m2.py
    - separateur_cadastre.py
"""
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


# ------------------- Merging Functions ------------------- #


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


def corr_type_de_voie(valeur_fonc_df):
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


# ------------------- TESTS ------------------- #


if __name__ == "__main__":
    # The latter will only run if the script called is this one (and not if the functions are reused elsewhere).

    # Testing normalization function
    string_to_norm = "Avenue du GÃ©nÃ©ral Leclerc"
    expected_string_norm = "av gen leclerc"
    print(
        "Normalisation Function test :",
        normalisation(string_to_norm) == expected_string_norm,
    )

    # Testing compare function
    ref_to_compare = "du GÃ©nÃ©ral Leclerc"
    comp_to_compare = "du GÃ©nÃ©ral Leclere"
    expected_compare = True
    print(
        "Compare Function test :",
        compare(12, "avenue", ref_to_compare, 12, "avenue", comp_to_compare)
        == expected_compare,
    )

    # Testing the cadastre df functions
    cadastre_df = pd.DataFrame(
        data={
            cad_street_full: ["Rue du Foin", "Avenue du Puit", "Boulevard de la Table"]
        }
    )
    expected_sep_street = pd.DataFrame(
        data={
            cad_street_type: ["Rue", "Avenue", "Boulevard"],
            cad_street_name: ["du Foin", "du Puit", "de la Table"],
        }
    )
    # Testing the valeur foncieres df functions
    df_valeur_fonciere = pd.DataFrame(
        data={
            vf_price_nominal: [100000, 500000, 450000, 375000],
            "Numero de voie": [0, 1, 14, 32],
            vf_street_type: ["Rue", "CHEM", "Rue", "BD"],
            vf_built_area: [10, 45, 30, 25],
        }
    )
    expected_df_norm = pd.DataFrame(
        data={
            vf_price_nominal: [100000, 500000, 450000, 375000],
            "Numero de voie": [0, 1, 14, 32],
            vf_street_type: ["Rue", "Chemin", "Rue", "Boulevard"],
            vf_built_area: [10, 45, 30, 25],
        }
    )
    expected_df_price = pd.DataFrame(
        data={
            vf_price_nominal: [100000, 500000, 450000, 375000],
            "Numero de voie": [0, 1, 14, 32],
            vf_street_type: ["Rue", "Chemin", "Rue", "Boulevard"],
            vf_built_area: [10, 45, 30, 25],
            vf_square_meter_price: [10000.0, 11111.0, 15000.0, 15000.0],
        }
    )
    # The assert_frame_equal function gives the discrepancies between two dataframes
    print(
        "Cadastre Street Type Separation :",
        assert_frame_equal(sep_voies(cadastre_df), expected_sep_street),
    )
    print(
        "Valeurs Foncieres Street Type Function test :",
        assert_frame_equal(corr_type_de_voie(df_valeur_fonciere), expected_df_norm),
    )
    print(
        "Valeurs Foncieres Square Meter price Function test :",
        assert_frame_equal(
            get_square_meter_price(df_valeur_fonciere), expected_df_price
        ),
    )
    # Testing the merge function
    df_cadastre = pd.DataFrame(
        data={
            cad_street_num: [4, 2, 11], 
            cad_street_type: ['rue', 'Boulevard', 'rue'], 
            cad_street_name: ['Vaugeirard', 'Maréchal Foche', 'Cournet'], 
            'Année': [1880, 1924, 1911],
        }
    )
    df_valeur_fonciere = pd.DataFrame(
        data={
            vf_street_num: [4 ,3, 11],  
            vf_street_type: ['rue', 'Avenue', 'rue'], 
            vf_street_name: ['vaugeirard', 'Maréchal Foche', 'Cournet'], 
            vf_built_area: [100, 45, 76],
            vf_price_nominal: [1000000, 550000, 950000],
        }
    )
    excpected_master_table_f = pd.DataFrame(
        data={
            cad_street_num: [4, 2, 11], 
            cad_street_type: ['rue', 'Boulevard', 'rue'], 
            cad_street_name: ['Vaugeirard', 'Maréchal Foche', 'Cournet'], 
            'Année': [1880, 1924, 1911],
            vf_built_area: [100, np.NaN, 76],
            vf_price_nominal: [100000, np.NaN, 950000],
        }
    )
    merger_output = merger(
        df_cadastre,
        df_valeur_fonciere,
        [vf_built_area, vf_price_nominal],
        [cad_street_num, cad_street_type, cad_street_name],
        [vf_street_num, vf_street_type, vf_street_name],
    )
    #print(merger_output.dtypes)
    #print(excpected_master_table_f.dtypes)
    int_cols = [cad_street_num, "Année"]
    float_cols = [vf_built_area, vf_price_nominal]
    for col in int_cols:
        merger_output[col] = merger_output[col].apply(int)
        excpected_master_table_f[col] = excpected_master_table_f[col].apply(int)
    for col in float_cols:
        merger_output[col] = merger_output[col].apply(float)
        excpected_master_table_f[col] = excpected_master_table_f[col].apply(float)
    print(
        "Merger test :",
        assert_frame_equal(
            merger_output,
            excpected_master_table_f,
        ),
    )
