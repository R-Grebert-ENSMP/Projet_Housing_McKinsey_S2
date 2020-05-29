import pandas as pd
import numpy as np

#DONNES POUR TEST---------------------------------------------------------------------------------------------------------------
d = {'Valeur Fonciere': [100000,500000,450000,375000],'Numero de voie' : [0,1,14,32],'Type de voie': ['Rue','Rue','Rue', 'BD'], 'Voie': ['Gen DG','Paix', '14 juillet','Europe']}
df1 = pd.DataFrame(data = d)

D = {'Valeur Fonciere': [100000,500000,450000,375000],'Numero de voie' : [0,1,14,32],'voie_nom': ['Rue du Gen DG','Rue de la Paix','Rue du 14 juillet', 'BD d Europe']}
Df1 = pd.DataFrame(data = D)

#-----------------------

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
