
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

#Code used to plot the prophet predictions


master_pred_2019 = pd.read_csv(r'C:\Users\Raphael\Desktop\ENSMP\COURS ENSMP\INFO ENSMP\INFO S2\prediction_2024.csv', sep =',')



master_pred_2019 = master_pred_2019[['x','y','mean_price_predicted']]
master_plot_2019 = master_pred_2019.pivot_table( index='y', columns='x', values='mean_price_predicted' )
master_plot_2019 = master_plot_2019.iloc[::-1 ]


#we plot a heatmap

p2=sns.heatmap(master_plot_2019, vmin=0, vmax=50000, xticklabels=5, yticklabels=5)

plt.show()