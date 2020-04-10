import pandas as pd

#pd.all=pd.read_csv('Desktop/valeursfoncieres-2015.txt', sep='|', engine='python')

def mask(df):
    master=pd.DataFrame(columns=df.columns)
    for i in range (75001, 75021):
        master=master.append(cond(df, 'Code postal', i))
    return master

def cond(df, key, value):
    return df[df[key] == value]

##
def duplica(df):
    master = df
    n = len(df.index)
    master.index = [i for i in range (n)]
    L = master['Surface reelle bati']
    i = 0
    while i < n-1:
        k = 1
        a = master.loc[i]['Surface reelle bati']
        if master.duplicated(['Valeur fonciere', 'Date mutation', 'Section'])[i]:
            while master.loc[i]['Section'] == master.loc[i+k]['Section']:
                a += master.loc[i+k]['Surface reelle bati']
                k += 1
        i += k
        L[i] = a
    return L

for i in L:
    if i%100==0:
        print(i)
    master_test['Surface reelle bati'].replace(master_test['Surface reelle bati'], i)
