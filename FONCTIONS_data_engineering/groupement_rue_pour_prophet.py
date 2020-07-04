import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import datetime


'''
the code below is our first try of making samples out of the master table for our machine learning baseline : the spatial samples are streets, and temporal samples are years.

'''



def group_by_roads(master_table):

    '''

    Parameter : the mastertable, of the VF from 2014 to 2018, following each other, merged on cadastre 75

    Returns : a new table where we have for each year and each street name only one value of price per square meter. The table  contains 6 columns : one for the street name , and the 5 average prices per squar meters of housing for each year. Prophet can then be applied to each row (bc prophet takes one 1d-array for values to predict and one 1d-array for time).

    NB : the columns street names of Master_table are the same as in cadastre (bc cadastre is used as a scaffold), which is why we will use the global_variables of cadaste here. We also use the column names of vf for the square meter price and year for the same reasons.


    '''

    #---------We select the data we want in the baseline and get rid of the problematic lines (NAs)

    master_table['vf_square_meter_price'] = master_table['vf_square_meter_price'].replace([np.inf, -np.inf], np.nan)
    master_table.dropna()

    columns  = ['Nom de voie','Type de voie','Date mutation','vf_square_meter_price']

    master_table = master_table[columns]

    #----------We recreate the "full adress" column, in order not to mistake (for instance) the "avenue gen de Gaulle" with the "rue gen de Gaulle", and create a "annee" column with only the year, in a correct format


    master_table['annee'] = pd.to_datetime(master_table['Date mutation'],format='%d/%m/%Y')

    master_table['annee'] = pd.DatetimeIndex(master_table['annee']).year

    master_table['full_street_name'] = master_table['Type de voie'] + master_table['Nom de voie']

    street_names = master_table['full_street_name'].unique()

    master_table = master_table.drop(columns=['Type de voie', 'Nom de voie'])

    #


    all_streets = []

    for name in street_names :


        #-------- let us create a df with all the rows which have the same full_street_name, and average the sq meter price on each road:

        id = []
        for i, st in enumerate(master_table['full_street_name']):
            if st == name :
                id.append(i)

        street = master_table.loc[id]

        street = street.groupby('annee')['vf_square_meter_price'].mean().reset_index()


        #---------We must ensure whether or not we have data for each year. If we dont, we keep the previous year's price per square meter
        #We go through each year to build the data we want : avg sqr meter price for each year

        years = street['annee'].unique()
        all_years = [2014,2015,2016,2017,2018]

        sqm_years = []

        for i,Y in enumerate(all_years) :


            if Y in years :

                for j, year_obj in enumerate(street['annee']):

                    if year_obj == Y :

                        sqm_years.append( (street.loc[j]['vf_square_meter_price']))


            if Y not in years :

                if sqm_years == []:

                    for j, year_obj in enumerate(street['annee']):

                        if year_obj == years[0] :

                            sqm_years.append( (street.loc[j]['vf_square_meter_price']))


                else :
                    sqm_years.append(sqm_years[-1])


        #-------- We build the data for each street, and then gather all streets and make a new Dataframe
        street_row = pd.DataFrame([sqm_years], index = [name] , columns = ['2014','2015','2016','2017','2018'])

        all_streets.append(street_row)

    master_table_streets = pd.concat(all_streets)


    return( master_table_streets )










## TEST ON THE 1ST ARROND MASTERTABLE // CAREFULLE : LOCAL ADRESS NEEDS TO BE CHANGED
master_1er_arrond = pd.read_csv('master_table_75001.csv', sep =',')

data = group_by_roads(master_1er_arrond)

print('-------------------')
print(data)

data.to_csv('data_baseline_75001.csv')


## TESTS : testing the function used to code "group_by_roads" on a small artificial dataframe



import datetime


df_test = pd.DataFrame([[12000,'12/05/2014','general', 'rue'],[7000,'12/05/2015','paix', 'rue'],[8500,'12/05/2016','marechal', 'rue'],[11000,'12/05/2015','paix', 'rue'],[14000,'12/05/2017','paix', 'rue'], [10500, '12/05/2016', 'general', 'rue']], index = [0, 1, 2, 3, 4,5], columns = ['price sq meter', 'time', 'Nom de voie', 'Type de voie'])


df_test['year'] = pd.to_datetime(df_test['time'],format='%d/%m/%Y')
df_test['year'] = pd.DatetimeIndex(df_test['year']).year


df_test['full_street_name'] = df_test['Type de voie'] + df_test['Nom de voie']

street_names = df_test['full_street_name'].unique()

all_streets_test = []

for name in street_names :

    id = []
    for i, st in enumerate(df_test['full_street_name']):
        if st == name :
            id.append(i)

    test = df_test.loc[id]

    print(pd.DataFrame(test))


    A = test.groupby('year')['price sq meter'].mean().reset_index()
    print('------------------------------ grpby')
    print(A)
    print('------------------------------ grpby-end')

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


    street_test = pd.DataFrame([sqm_years], index = [name] , columns = ['2014','2015','2016','2017','2018'])


    all_streets_test.append(street_test)

master_street_test = pd.concat(all_streets_test)
print(master_street_test)

print('----------------------------------', df_test,'----------------------------------', df_test['Nom de voie'][1])

#The code is working like we want