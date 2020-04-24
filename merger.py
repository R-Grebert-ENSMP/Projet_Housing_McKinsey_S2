import pandas as pd
import numpy as np
import jellyfish
import nltk
from Desktop.Projet_Housing_McKinsey_S2.compareadresse import compare, normalisation

master1 = pd.DataFrame({'Num': [4 ,2,11], 'Type': ['rue', 'Boulevard', 'rue'], 'Voie': ['Vaugeirard', 'Maréchal Foche', 'Cournet'], 'Année': [1880, 1924, 1911]})

master2 = pd.DataFrame({'Num': [4 ,3, 11],  'Type': ['rue', 'Avenue', 'rue'], 'Voie': ['vaugeirard', 'Maréchal Foche', 'Cournet'], 'Surface': [100, 45, 76], 'Valeur fonciere': [1000000, 550000, 950000]})
##
def merger(df1, df2, c_merger, c_compare):
    res = df1.copy()
    long_c_merger = len(c_merger)
    for i in c_merger:
        res[i] = np.NaN
    M1 = np.array(df1)
    M2 = np.array(df2) #On passe en numpy
    R = np.array(res)
    columns_df1 = list(df1.columns)
    columns_df2 = list(df2.columns)
    columns_res = list(res.columns)
    indexem_c_df2 = [columns_df2.index(i) for i in c_merger] # Indice des colonnes à merge DANS df2
    indexem_c_res = [columns_res.index(i) for i in c_merger] # Indice des colonnes à merge DANS res
    #Ces listes d'indice sont nécessaires afin d'accéder aux bonnes colonnes dans numpy
    indexec_c_df1 = [columns_df1.index(i) for i in c_compare] #indice des colonnes à comparer DANS df1
    indexec_c_df2 = [columns_df2.index(i) for i in c_compare] #indice des colonnes à comparer DANS df2
    a = len(M1[:,0]) # b de ligne de M1
    b = len(M1[:,0]) #Nb de ligne de M2
    for i in range (a):
        (Num1, Type1, Voie1) = (M1[i, p] for p in indexec_c_df1)
        for j in range (b):
            (Num2, Type2, Voie2) = (M2[j, p] for p in indexec_c_df1)
            if compare(Num1, Type1, Voie1, Num2, Type2, Voie2):
                for k in range (long_c_merger):
                    R[i, indexem_c_res[k]] = M2[j, indexem_c_df2[k]]
    res_f = pd.DataFrame(R)
    res_f.columns = res.columns
    return res_f

