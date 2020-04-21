import pandas as pd
import time

pd.all=pd.read_csv('Desktop/valeursfoncieres-2015.txt', sep='|', engine='python')


df['prix_m2'] = df['Valeur fonciere']/(df['Surface reelle batie'])
