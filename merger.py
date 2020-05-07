import pandas as pd
import numpy as np
import jellyfish
import nltk
from Desktop.Projet_Housing_McKinsey_S2.compareadresse import compare, normalisation

master1 = pd.DataFrame({'Num': [4 ,2,11], 'Type voie': ['rue', 'Boulevard', 'rue'], 'Nom voie': ['Vaugeirard', 'Maréchal Foche', 'Cournet'], 'Année': [1880, 1924, 1911]})

master2 = pd.DataFrame({'Numero': [4 ,3, 11],  'Type': ['rue', 'Avenue', 'rue'], 'Voie': ['vaugeirard', 'Maréchal Foche', 'Cournet'], 'Surface': [100, 45, 76], 'Valeur fonciere': [1000000, 550000, 950000]})
##
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

def merger(clean_cadastre, clean_valeur_fonc, columns_merger, columns_cadastre_compare, columns_vf_compare):
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

