from math import sin, cos, sqrt, atan2, radians
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt



def dist_coord(lt1,lg1,lt2,lg2):
    '''
    Returns the distance in kilometers between two point, given their respective latitude and longitude

    '''
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lt1)
    lon1 = radians(lg1)
    lat2 = radians(lt2)
    lon2 = radians(lg2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance


# Example--------------------------------
# lat1 = (52.2296756)
# long1 = (21.0122287)
# lat2 = (52.406374)
# long2 = (16.9251681)
#
# print(dist_coord(lat1,long1,lat2,long2))
#----------------------------------------


def add_exo_colleges(master_table, college_table):

    '''
    Merges a master_table from the pipeline (which is cadastre75 merged with VF), with the "etablissement-scolaire-college" table. I

    It creates a new column "middle_school" in the master table, that gives the amount of middle school in 1 km around each adress

    '''
    L = master_table.shape[0]

    N = college_table.shape[0]
    #we create a full of 0 column for now

    master_table ['middle_school'] = [0 for k in range(L)]

    for i in range(L) :

        for j in range(N) :

            if dist_coord(master_table['long'][i],master_table['lat'][i],college_table['long'][j],college_table['lat'][j]) <= 1 :

                 master_table ['middle_school'][i] += 1

    return master_table

def add_exo_metros(master_table, metro_table):

    '''
    Merges a master_table from the pipeline (which is cadastre75 merged with VF), with the "plan-de-voirie-acces-pietons-metro-et-parkings" table. I

    It creates a new column "acces_metros" in the master table, that gives the amount of metro entrances in 1 km around each adress

    '''
    L = master_table.shape[0]

    N = metro_table.shape[0]
    #we create a full of 0 column for now

    master_table ['acces_metros'] = [0 for k in range(L)]

    for i in range(L) :

        for j in range(N) :

            if dist_coord(master_table['long'][i],master_table['lat'][i],metro_table['long'][j],metro_table['lat'][j]) <= 1 :

                 master_table ['middle_school'][i] += 1

    return master_table

def add_exo_commerces(master_table, commerces_table):

    '''
    Merges a master_table from the pipeline (which is cadastre75 merged with VF), with the "etalages-et-terrasses" table. I

    It creates a new column "commerces" in the master table, that gives the amount of grocery shops, restaurants, cafes in 1 km around each adress

    '''
    L = master_table.shape[0]

    N = commerces_table.shape[0]

    #we create a full of 0 column for now

    master_table ['commerces'] = [0 for k in range(L)]

    for i in range(L) :

        for j in range(N) :

            if dist_coord(master_table['long'][i],master_table['lat'][i],commerces_table['long'][j],commerces_table['lat'][j]) <= 1 :

                 master_table ['middle_school'][i] += 1
    return master_table

##test ATTENTION CHEMINS LOCAUX A REDEFINIR SUR VOTRE APPAREIL

 #attention au sep = ';'   !!!!!!!!!!!!!!!!!!!!!!

master_1er_arrond = pd.read_csv(r'C:\Users\Raphael\Desktop\ENSMP\COURS ENSMP\INFO ENSMP\INFO S2\master_table_75001.csv')

commerce_table = pd.read_csv(r'C:\Users\Raphael\Desktop\ENSMP\COURS ENSMP\INFO ENSMP\INFO S2\etalages-et-terrasses.csv', sep =';')

metro_table = pd.read_csv(r'C:\Users\Raphael\Desktop\ENSMP\COURS ENSMP\INFO ENSMP\INFO S2\plan-de-voirie-acces-pietons-metro-et-parkings.csv', sep =';')

college_table = pd.read_csv(r'C:\Users\Raphael\Desktop\ENSMP\COURS ENSMP\INFO ENSMP\INFO S2\etablissements-scolaires-colleges.csv', sep =';')


master_0 = add_exo_colleges(master_1er_arrond,college_table)

master_1 = add_exo_metros(master_0,metro_table)

new_master = add_exo_commerces(master_1,college_table)

print(new_master)














