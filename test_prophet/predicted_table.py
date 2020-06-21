import numpy as np
import pandas as pd
from fbprophet import Prophet
import datetime
import matplotlib.pyplot as plt
from fbprophet.diagnostics import performance_metrics
from fbprophet.diagnostics import cross_validation
m = Prophet()

#older mean prices add to our recent and precise data to have less biased preditions
m2_1er_1993_2013 = [2650, 3490, 2880, 2670, 2420, 2710, 2730, 3350, 3830, 3790, 4650, 5330, 5910, 6800, 7220, 8980, 8390, 8330, 9750, 10760, 10150]

#create dataframe with predictions for 2019 (2018-12-31)
predictions_2019 = []

for (x,y) in ... :
    unique_row = master_ord[(master_ord['lat'] = x) & (master_ord['long'] = y)]
    data = {'ds' : [datetime.date(k, 1, 1) for k in range(1993, 2019)], 'y' : m2_1er_1993_2013 + [unique_row[f"{year}"][0] for year in range(2014, 2019)]}
    
    df = pd.DataFrame(data, columns = ['ds', 'y'])
    m.fit(df)
    future_years = m.make_future_dataframe(periods = 4, freq = 'Y')

    forecast_years = m.predict(future_years)
    forecast_years[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

    #comparison with the real 2018
    df_cv = cross_validation(m, horizon = 10, period = '365,25 days')

    #prediction model evalution
    df_p = performance_metrics(df_cv)

    predictions_2019.append([lat, long, forecast_years["yhat"][26], forecast_years["yhat_lower"][26],forecast_years["yhat_upper"][26], df_p["rmse"][0]])

df_pred = pd.DataFrame(predictions_2019, columns=['lat', 'long', 'mean_price_predicted', 'mean_price_predicted_lower', 'mean_price_predicted_upper', 'rmse'])
print(df_pred)