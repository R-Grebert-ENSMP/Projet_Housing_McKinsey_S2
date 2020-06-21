import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

master = pd.read_csv(r'C:\Users\Raphael\Desktop\ENSMP\COURS ENSMP\INFO ENSMP\INFO S2\master_table_75001_2014.csv')
master['vf_square_meter_price'] = master['vf_square_meter_price'].replace([np.inf, -np.inf], 0)
master = master.loc[(master['vf_square_meter_price']>5000)]
master = master.loc[(master['vf_square_meter_price']<100000)]#Filter the wring prices, prices under 5k€ square meter and above 100k

#annual filter : we create a column with only the year, and then filter the mastertable on a certain year
master['annee'] = pd.to_datetime(master['Date mutation'],format='%d/%m/%Y')
master['annee'] = pd.DatetimeIndex(master['annee']).year
master = master.loc[(master['annee'] == 2018)]

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
division = 40
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

#print(master_quadrille)

#print(master_cadrille.columns)

#
# print(master_cadrille.head()['bottom_left'])
# print(master_cadrille.head()['bottom_right'])
# print(master_cadrille.head()['top_left'])
#print(master_cadrille['top_right'])


# WE ARE NOW GOING TO MAKE A GRID OF X AND Y COORDINATES WITH EACH A VALUE


#--------------------- we create x and y coordinates---------------
master_quadrille['x'] = [np.array(0) for k in range(len(master_quadrille['bottom_right']))]
for i,x in enumerate(master_quadrille['x']):


    master_quadrille['x'][i] = (master_quadrille['bottom_right'][i][1] + master_quadrille['bottom_left'][i][1] )/2



master_quadrille['y'] = [np.array(0) for k in range(len(master_quadrille['bottom_right']))]
for i,y in enumerate(master_quadrille['y']):


    master_quadrille['y'][i]  = (master_quadrille['bottom_right'][i][0] + master_quadrille['top_left'][i][0] )/2

print(master_quadrille)

print(master_quadrille['y'][4].type())

##BUILDING DATA FOR PROPHET
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
        print(line)

        bloc = pd.DataFrame([line], index = [f'{x},{y}'] , columns = ['x','y','2014','2015','2016','2017','2018'])
        master_ord.append(bloc)

master_ord = pd.concat(master_ord)


print(master_ord)
##
M = master_ord.copy()

##PLOTTING YEAR  2014 - 2018
#----------------------------we use these coordinate to create a new dataframe with only x, y and square meter price values (and reverse it to have a geographically coherent map in the end)
master_plot = master_quadrille.pivot_table( index='y', columns='x', values='square_meter_price' )

master_plot = master_plot.iloc[::-1 ]


#we plot a heatmap
p2=sns.heatmap(master_plot)
plt.show()
