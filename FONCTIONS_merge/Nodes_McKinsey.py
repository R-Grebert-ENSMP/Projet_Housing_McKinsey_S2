import pandas as pd


from loader import Loader
df_all = pd.read_csv('data/output/DVF_Paris_v4.csv')
df_master_2 = df_all.dropna(subset=["Lat", "Long"])

def merger2(
    f: pd.DataFrame, p: pd.DataFrame, l, r=None
) -> pd.DataFrame:
    master_table = f.merge(p, left_on="l", right_on="r")
    return master_table

def selection(f: pd.DataFrame, **kwargs):
    return f.dropna(subset[i for i in **kwargs])

def drop_duplica(f: pd.DataFrame,**kwargs):
    return f[[i for i in **kwargs]].drop_duplicates()

def data_add(f: pd.DataFrame, data):
    return 

    

def create_pipeline(**kwargs):
    return Pipeline (
    [
        node(func=merger,
            inputs='',
            outputs='',
            name='',
        )
    ]#Schéma à reproduire à la suite pour merge plusieurs tableau 
    
    
#Création des Nodes
#Début du Pipeline (à poursuivre si les nodes sont bons)
#Q: Peut on utiliser les fonctions panda dans les nodes ? 
#Q: 