import numpy as np
import pandas as pd
from fbprophet import Prophet
import datetime
import matplotlib.pyplot as plt

m2_1er_93_13 = [2650, 3490, 2880, 2670, 2420, 2710, 2730, 3350, 3830, 3790, 4650, 5330, 5910, 6800, 7220, 8980, 8390, 8330, 9750, 10760, 10150]

data = {'ds' : [datetime.date(k, 1, 1) for k in range(1993, 2019)], 'y' : m2_1er_93_13 + [9800, 9200, 10710, 12040, 11560]}
#data = {'ds' : [datetime.date(k, 1, 1) for k in range(1993, 2019)], 'y' : m2_1er_93_13 + [master_cadrille[f"{year}"]["idx"] for year in range(2014, 2019)]}
df = pd.DataFrame(data, columns = ['ds', 'y'])

m = Prophet()
m.fit(df)
future_years = m.make_future_dataframe(periods = 4, freq = 'Y')

forecast_years = m.predict(future_years)
forecast_years[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
print(forecast_years)

fig1 = m.plot(forecast_years)
fig2 = m.plot_components(forecast_years)

#comparison with the real fifth year
from fbprophet.diagnostics import cross_validation
df_cv = cross_validation(m, horizon = 10, period = '365,25 days')
print(df_cv)

#prediction model evalution
from fbprophet.diagnostics import performance_metrics
df_p = performance_metrics(df_cv)
print(df_p.head())


#create dataframe with predictions for 2019 (2018-12-31)
predictions_2019 = []
lat = 2.2
long = 3.3
#code
    #for (x,y) in ... :
    #unique_row = master_ord[(master_ord['lat'] = x) & (master_ord['long'] = y)]
    #data = {'ds' : [datetime.date(k, 1, 1) for k in range(1993, 2019)], 'y' : m2_1er_93_13 + [unique_row[f"{year}"][0] for year in range(2014, 2019)]}
    #prophet
predictions_2019.append([lat, long, forecast_years["yhat"][26], forecast_years["yhat_lower"][26],forecast_years["yhat_upper"][26], df_p["rmse"][0]])
df_pred = pd.DataFrame(predictions_2019, columns=['lat', 'long', 'mean_price_predicted', 'mean_price_predicted_lower', 'mean_price_predicted_upper', 'rmse'])
print(df_pred)

plt.show()