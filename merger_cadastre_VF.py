import pandas as pd
from Codes Selection Paris import all

dfVF = pd.read_csv('', sep='|', engine='python')
dfCAD = pd.read_csv('Desktop/adresse-cadastre-75.txt', sep=';', engine='python')


# il faut appliquer tous les traitements intermediaires (fonctions de stop words, normalisation,



#ensuite on découpe par arrondissement et on merge arrondissement par arrondissement en colonne, avec la fonction de coco
for i in range 20 :
    cad =
    vf =

    merge_col_arr =  cad.merge(vf,left_index = ['numero', 'Nom voie', 'Type de voie'], right_index = ['No voie', 'Type de voie', 'Voie'])

#ensuite on recolle par arrondissement dans l'ordre