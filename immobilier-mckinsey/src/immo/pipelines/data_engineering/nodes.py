import json
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import folium
from shapely.geometry import Point, Polygon
import geopandas

def cond(df, code_postal, arrond):
    """Le but de cond est de selectionner la partie du tableau correspond au code postal voulue"""
    return df[df[code_postal] == arrond]


def duplica(df_paris):
    """duplica prend en entrée une partie de valeur fonciere, additionne les surface d'un même lot et supprime les lignes non nécessaires de ce lot afin d'avoir une unique ligne par adresse"""
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


def sep_voies(df):
    '''
    Prends en entrée cadastre 75 et sépare la colonne 'voie_nom' en 'Type de voie' et 'Nom de voie'

    '''
    TDV = []
    NV = []
    for i in df['voie_nom']:

        a = i.split(' ')
        TDV.append(a[0])
        a.pop(0)
        a = " ".join(a)
        NV.append(a)

    out = pd.DataFrame({'Nom voie': TDV, 'Type de voie': NV})
    for c in df.columns:
        if c != 'voie_nom' :
            out[c] = df[c]

    return out


def corr_type_de_voie(df):
    '''

    Prends en entree un valeur foncière trié sans doublon sur Paris et remplace les types de voie pour qu'on puisse les comparer a ceux de  cadastre 75 (ex transforme BV en Boulevard...)

    '''
    Tdvoie_corr = []
    for i in df['Type de voie']:
        if i =='BD':
            i = 'Boulevard'
        if i == 'AV':
            i = 'Avenue'
        if i == 'RTE':
            i = 'Route'
        if i == 'CHEM':
            i = 'Chemin'
        if i == 'IMP':
            i = 'Impasse'
        if i == 'PL':
            i = 'Place'
        Tdvoie_corr.append(i)

    table = pd.DataFrame({'Nom voie': Tdvoie_corr})
    for c in df.columns:
        if c != 'Type de voie' and c != 'Voie' :
            table[c] = df[c]
    return table
    

def accent(string):
    """remplace les mauvais caractère de la table valeurfoncière"""
    old = ['Ã©','Ã¨','Ã´','Ã¢','Ã»',"Ãª","'"]
    new = ['e','e','o','a','u','e',' ']
    for i in range(len(old)):
        string = str.replace(string, old[i], new[i])
    return string


def deletewords(string):
    """supprime les mots tels que "de" "la" "du"... pour comparer plus facilement"""
    sw = list(stopwords.words('french'))
    listwords = str.split(string)
    i = 0
    while i < len(listwords):
        if listwords[i] in sw :
            del listwords[i]
        else : 
            i += 1
    string = " ".join(listwords)
    return string


def normalisation_adresse(voie) : 
    voie = accent(voie)
    voie = voie.lower()
    voie = deletewords(voie)
    return voie


def compare(num1, type1, voie1, num2, type2, voie2):
    """compare l'adresse de 2 lignes afin de savoir si ce sont les mêmes"""
    voie1 = normalisation_adresse(voie1)
    # normalise l'écriture, minuscule sans accent, sans apostrophe, sans stopwords
    voie2 = normalisation_adresse(voie2)
    distance = jellyfish.jaro_distance(normalisation_adresse(voie1), normalisation_adresse(voie2))
    if num1==num2 and type1==type2 and distance > 0.8 :
        #possibilité de rajouter une sélection sur la distance minimale
        return True
    else : 
        return False