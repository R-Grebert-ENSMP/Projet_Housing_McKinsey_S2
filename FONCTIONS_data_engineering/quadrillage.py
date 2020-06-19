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
lat_idx = columns.index('lat')
long_idx = columns.index('long')
square_meter_price_idx = columns.index('vf_square_meter_price')

master_cadrille = pd.DataFrame(columns = ['bottom_left','bottom_right', 'top_right', 'top_left', 'square_meter_price'])
k = 0
division = 40
division_lat = np.linspace(min_lat, max_lat, division+1)
division_long = np.linspace(min_long, max_long, division+1)
P_lat = M[M[:, lat_idx] < division_lat[1]]
P = P_lat[P_lat[:, long_idx] < division_long[1]]

for i in division_lat[1:]:
    for j in division_long[1:]:
        M_filter = M[np.logical_and(M[:, lat_idx] < i, M[:, long_idx] < j)]
        idx_to_delete = np.where(M[np.logical_and(M[:, lat_idx] < i, M[:, long_idx] < j)])
        if len(M_filter) != 0:
            l = len(M_filter) #Get the number of lines
            mean_price = sum(M_filter[:, square_meter_price_idx])/l
            master_cadrille.loc[k] = [(i-1, j-1), (i-1, j), (i, j), (i, j-1), mean_price]
            np.delete(M, idx_to_delete) #delete the elements already used
        k += 1


master_cadrille = master_cadrille.reset_index()

#print(master_cadrille.columns)

#
# print(master_cadrille.head()['bottom_left'])
# print(master_cadrille.head()['bottom_right'])
# print(master_cadrille.head()['top_left'])
#print(master_cadrille['top_right'])


# WE ARE NOW GOING TO MAKE A GRID OF X AND Y COORDINATES WITH EACH A VALUE


#--------------------- we create x and y coordinates---------------
master_cadrille['x'] = [np.array(0) for k in range(len(master_cadrille['bottom_right']))]
for i,x in enumerate(master_cadrille['x']):


    master_cadrille['x'][i] = (master_cadrille['bottom_right'][i][1] + master_cadrille['bottom_left'][i][1] )/2



master_cadrille['y'] = [np.array(0) for k in range(len(master_cadrille['bottom_right']))]
for i,y in enumerate(master_cadrille['y']):


    master_cadrille['y'][i]  = (master_cadrille['bottom_right'][i][0] + master_cadrille['top_left'][i][0] )/2

#print(master_cadrille)

#----------------------------we use these coordinate to create a new dataframe with only x, y and square meter price values (and reverse it to have a geographically coherent map in the end)
master_plot = master_cadrille.pivot_table( index='y', columns='x', values='square_meter_price' )

master_plot = master_plot.iloc[::-1 ]


#we plot a heatmap
p2=sns.heatmap(master_plot)
plt.show()
