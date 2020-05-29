import pandas as pd
import numpy as np
# for i in range(4) :
#     pd.all=pd.read_csv(f'Desktop/valeursfoncieres-{2014+i}.txt', sep='|', engine='python')
#

#DONNES POUR TEST---------------------------------------------------------------------------------------------------------------
d = {'Valeur Fonciere': [100000,500000,450000,375000],'Numero de voie' : [0,1,14,32],'Type de voie': ['Rue','Rue','Rue', 'BD'], 'Voie': ['Gen DG','Paix', '14 juillet','Europe']}
df1 = pd.DataFrame(data = d)

D = {'Valeur Fonciere': [100000,500000,450000,375000],'Numero de voie' : [0,1,14,32],'voie_nom': ['Rue du Gen DG','Rue de la Paix','Rue du 14 juillet', 'BD d Europe']}
Df1 = pd.DataFrame(data = D)

#--------------------------------------------------------------------------------------------------------------------------------

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

