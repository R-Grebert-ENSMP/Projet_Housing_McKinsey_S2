import pandas as pd

import time

pd.all=pd.read_csv('Desktop/valeursfoncieres-2015.txt', sep='|', engine='python')

##
def mask_vf(df):
    df_paris = pd.DataFrame(columns = df.columns)
    for i in range (75001, 75021):
        df_paris = master.append(cond(df, 'Code postal', i))
    return df_paris

def cond(df, code_postal, arrond):
    return df[df[code_postal] == arrond]

def duplica(df_paris):
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


