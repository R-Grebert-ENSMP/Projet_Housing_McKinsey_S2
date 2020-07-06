import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt




#carefull_ : local path !!!
master = pd.read_csv(r'C:\Users\Raphael\Desktop\ENSMP\COURS ENSMP\INFO ENSMP\INFO S2\master_table_75001_2014.csv')
#!!!




def quad(df, Y=None, D = 40):

    '''
    This function is used to implement our final choice of spacial sampling : we discretize a zone (we worked on the 1st disctrict of Paris) with a grid, based on the latitude and longitude.

    Parameters : a master table data frame (from our kedro pipeline), the year for which we want to have a sampling and D the number of divions we want for our grid (grid sized DxD)

    Returns : the sampled grid : returns a df of DxD lines, each one with columns containing:  its year, its avg square meter price on the year, the coordinates of each of its corner, and the coordinates x and y of its center.

    '''


    master = df
    master['vf_square_meter_price'] = master['vf_square_meter_price'].replace([np.inf, -np.inf], 0)
    master = master.loc[(master['vf_square_meter_price']>5000)]
    master = master.loc[(master['vf_square_meter_price']<100000)]#Filter the wring prices, prices under 5k€ square meter and above 100k

    #annual filter : we create a column with only the year, and then filter the mastertable on a certain year
    master['annee'] = pd.to_datetime(master['Date mutation'],format='%d/%m/%Y')
    master['annee'] = pd.DatetimeIndex(master['annee']).year

    #this line below allows the choice of the year
    if Y != None:
        master = master.loc[(master['annee'] == Y)]


    #---------------------------Creating the spatial grid---------------------------------------------------
    max_lat = master['lat'].max()
    min_lat = master['lat'].min()
    max_long = master['long'].max()
    min_long = master['long'].min()

    M = np.array(master)
    columns = list(master.columns)
    date_idx = columns.index('Date mutation')
    lat_idx = columns.index('lat')
    long_idx = columns.index('long')
    square_meter_price_idx = columns.index('vf_square_meter_price')

    master_quadrille = pd.DataFrame(columns = ['year', 'bottom_left','bottom_right', 'top_right', 'top_left', 'square_meter_price'])
    division = D
    division_lat = np.linspace(min_lat, max_lat, division+1)
    division_long = np.linspace(min_long, max_long, division+1)
    k = 0

    for year in ['2014', '2015', '2016', '2017', '2018']:
        M_year = np.array(master[master['Date mutation'].str.contains(year)])
        for i in division_lat[1:]:
            for j in division_long[1:]:
                M_filter = M_year[np.logical_and(M_year[:, lat_idx] < i, M_year[:, long_idx] < j)]
                idx_to_delete = np.where(M[np.logical_and(M[:, lat_idx] < i, M[:, long_idx] < j)])
                if len(M_filter) != 0:
                    l = len(M_filter) #Get the number of lines
                    mean_price = sum(M_filter[:, square_meter_price_idx])/l
                    master_quadrille.loc[k] = [year, (i-1, j-1), (i-1, j), (i, j), (i, j-1), mean_price]
                    np.delete(M_year, idx_to_delete) #delete the elements already used
                k += 1


    master_quadrille = master_quadrille.reset_index()

    # WE ARE NOW GOING TO MAKE A GRID OF X AND Y COORDINATES WITH EACH A VALUE
    #--------------------- we create x and y coordinates---------------
    master_quadrille['x'] = [np.array(0) for k in range(len(master_quadrille['bottom_right']))]
    for i,x in enumerate(master_quadrille['x']):


        master_quadrille['x'][i] = (master_quadrille['bottom_right'][i][1] + master_quadrille['bottom_left'][i][1] )/2



    master_quadrille['y'] = [np.array(0) for k in range(len(master_quadrille['bottom_right']))]
    for i,y in enumerate(master_quadrille['y']):


        master_quadrille['y'][i]  = (master_quadrille['bottom_right'][i][0] + master_quadrille['top_left'][i][0] )/2

    return(master_quadrille)






master_quadrille = quad(master)
print(master_quadrille)




#--------------------------------------------------------------------------------------
#What are the dimensions of one square of the grid? code below to answer this question
#--------------------------------------------------------------------------------------
from math import sin, cos, sqrt, atan2, radians

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
a = master_quadrille['top_left'][5]
b = master_quadrille['top_right'][5]

print('-----------------One grids square measures ')
print(dist_coord(a[0],a[1],b[0],b[1]), 'meters')

#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------









def prophet_builder(master_quadrille):
    '''
    builds a dataframe that can be read by prophet

    parameters : a grid from quad()

    returns : a df with the squares of the grid as indexes, and the years, x and ys coordinates of the grid's square as columns.
    Each line can thus be interpreted for the fb prophet predictions

    '''
    X = master_quadrille['x'].unique()
    Y = master_quadrille['y'].unique()
    master_ord = []

    all_years = [2014,2015,2016,2017,2018]

    for i,x in enumerate(X) :

        for j,y in enumerate(Y):

            line = [x,y]
            s = 2013
            for year in all_years :


                for k,p in enumerate(master_quadrille['square_meter_price']):

                    if master_quadrille['x'][k] == x:

                        if master_quadrille['y'][k] == y:

                            if int(master_quadrille['year'][k]) == year:

                                if year == s + 1:
                                    s = year
                                    line.append(p)
                                else :
                                    if len(line)==2:
                                        line.append(0)
                                    else :
                                        line.append(line[-1])


            if len(line) <= 7:
                for k in range(7- len(line)):
                    line.append(0)

            bloc = pd.DataFrame([line], index = [f'{x},{y}'] , columns = ['x','y','2014','2015','2016','2017','2018'])
            master_ord.append(bloc)

    master_ord = pd.concat(master_ord)

    return(master_ord)

master_ord = prophet_builder(master_quadrille)
print(master_ord)





def map_plot(master_ord):
    '''
    Builds a heatmap, displaying the grid visually to see the square meter prices in the district
    The x and y coordinates are used to plot the map.
    NB : This function is used to plot the existant data (2014 -> 2018). The predictions are made with another file ('predicted_table'), saved, and plotted with the 'plot' file.


    parameters : a grid from master_quadrille

    returns : heatmap
    '''



    master_plot = master_quadrille.pivot_table( index='y', columns='x', values='square_meter_price' )

    master_plot = master_plot.iloc[::-1 ]


    #we plot a heatmap
    p2=sns.heatmap(master_plot,vmin=0, vmax=50000, xticklabels=5, yticklabels=5)
    plt.show()
