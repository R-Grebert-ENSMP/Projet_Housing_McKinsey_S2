# Column Names
# Valeurs Foncieres table
vf_street_num = "No voie"
vf_street_type = "Type de voie"
vf_price_nominal = "Valeur fonciere"
vf_built_area = "Surface reelle bati"
vf_square_meter_price = "prix_m2"
vf_street_name = "Voie"
# Cadastre table
cad_street_full = "voie_nom"
cad_street_type = "Type de voie"
cad_street_name = "Nom voie"
cad_street_num = "numero"

# Addresses Normalization
norm_street_types = {
    "BD": "Boulevard",
    "AV": "Avenue",
    "RTE": "Route",
    "CHEM": "Chemin",
    "IMP": "Impasse",
    "PL": "Place",
}
norm_accents = {
    'Ã©':'e',
    'Ã¨':'e',
    'Ã´':'o',
    'Ã¢':'a',
    'Ã»':'u',
    "Ãª":'e',
}
norm_abbrevations = {
    "general": "gen",
    "place": "pl",
    "impasse": "imp",
    "docteur": "doc",
    "saint": "st",
    "route": "ret",
    "boulevard": "bd",
    "avenue": "av",
    "allee": "all",
    "sentier": "sen",
    "chemin": "che",
    "lotissement": "lot",
    "passage": "pas",
    "promenade": "prom",
}
stop_words = ["de", "du", "la", "des", "d'", "l'", "les", "le", "la"]