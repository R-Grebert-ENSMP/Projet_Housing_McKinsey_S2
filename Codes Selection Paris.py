pd.all=pd.read_csv('Desktop/valeursfoncieres-2015.txt', sep='|', engine='python')

def mask(df):
    master=pd.DataFrame(columns=df.columns)
    for i in range (75001, 75021):
        master=master.add(cond(df, 'Code postal', i), axis=1)
    return master

def cond(df, key, value):
    return df[df[key] == value]

def duplicat(df):
    