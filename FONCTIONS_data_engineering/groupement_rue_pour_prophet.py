import pandas as pd
#from immo.pipelines.data_engineering.global_variables import parameters
import numpy as np
import math
import matplotlib.pyplot as plt
import folium
from shapely.geometry import Point, Polygon
import geopandas





def group_by_roads(master_table):

    '''

    Parameter : the mastertable, of the VF from 2014 to 2018, following each other, merged on cadastre 75

    Returns : a new table where we have for each year and each street name only one value of price per square meter. The table  contains 6 columns : one for the street name , and the 5 average prices per squar meters of housing for each year. Prophet can then be applied to each row (bc prophet takes one 1d-array for values to predict and one 1d-array for time).

    NB : the columns street names of Master_table are the same as in cadastre (bc cadastre is used as a scaffold), which is why we will use the global_variables of cadaste here. We also use the column names of vf for the square meter price and year for the same reasons.


    '''

    #We recreate the "full adress" column, in order not to mistake (for instance) the "avenue gen de Gaulle" with the "rue gen de Gaulle"
    master_table['full_street_name'] = master_table[parameters["cad_street_name"]] + master_table[parameters["cad_street_type"]]

    street_names = master_table[parameters["full_street_name"]].unique()

    all_streets = []

    for name in street_names :

        street = master_table.loc[ master_table['full_street_name'] == name ] #created a df with all the rows which have the same full_street_name
        street.groupby(parameters["vf_date"])[parameters["vf_square_meter_price"]].mean().reset_index() #groups the rows by individual year of sale, and keeps the average of their square meter price


        #We must ensure whether or not we have data for each year. If we dont, we keep the previous year's price per square meter
        years = street[parameters["vf_date"]].unique()
        all_years = [2014,2015,2016,2017,2018]

        sqm_years = []

        for i,Y in enumerate(all_years) :

            if Y in years :
                sqm_years.append( (street.loc[ lambda street: street[parameters["vf_date"]] == Y ][parameters["vf_square_meter_price"]]).iloc[0] )

            if Y not in years :

                if sqm_years == []:
                    sqm_years.append((A.loc[ lambda street: street['year'] == years[0]])[parameters["vf_square_meter_price"]].iloc[0])

                else :
                    sqm_years.append(sqm_years[-1])


        street_row = pd.DataFrame([sqm_years], index = [name] , columns = ['2014','2015','2016','2017','2018'])

        all_streets.append(stree_row)

    master_table_streets = pd.concat(all_streets)


    return( master_table_streets )







## test pour verifier le fonctionnement du code
df_test = pd.DataFrame([[12000,2014,'rue du general'],[7000,2015,'rue de la paix'],[8500,2016,'rue du marechal'],[11000,2015,'rue de la paix'],[9000,2017,'rue de la paix'], [10500, 2016, 'rue du general']], index = [0, 1, 2, 3, 4,5], columns = ['price sq meter', 'year', 'full_street_name'])


street_names = df_test['full_street_name'].unique()

all_streets_test = []

for name in street_names :
    test = df_test.loc[lambda df_test: df_test['full_street_name'] == name]
    #print(test)

    A = test.groupby('year')['price sq meter'].mean().reset_index()



    years = A['year'].unique()
    all_years = [2014,2015,2016,2017,2018]

    sqm_years = []

    for i,Y in enumerate(all_years) :

        if Y in years :
            sqm_years.append( ((A.loc[ lambda A: A['year'] == Y])['price sq meter']).iloc[0] )

        if Y not in years :
            if sqm_years == []:
                sqm_years.append((A.loc[ lambda A: A['year'] == years[0]])['price sq meter'].iloc[0])

            else :
                sqm_years.append(sqm_years[-1])

    #print(sqm_years)

    street_test = pd.DataFrame([sqm_years], index = [name] , columns = ['2014','2015','2016','2017','2018'])

    all_streets_test.append(street_test)

master_street_test = pd.concat(all_streets_test)
print(master_street_test)
