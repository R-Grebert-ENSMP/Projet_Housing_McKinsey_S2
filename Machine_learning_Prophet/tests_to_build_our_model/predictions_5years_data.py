import numpy as np
import pandas as pd
from fbprophet import Prophet
import datetime
import matplotlib.pyplot as plt


data = {'ds' : [datetime.date(k, 1, 1) for k in range(2014, 2019)], 'y' : [8000, 8100, 8900, 9500, 10200]}
#data = {'ds' : [datetime.date(k, 1, 1) for k in range(2014, 2019)], 'y' : [master_cadrille["mean_price"][where x=..., y=...], 8100, 8900, 9500, 10200]}
df = pd.DataFrame(data, columns = ['ds', 'y'])

m = Prophet()
m.fit(df)
future_years = m.make_future_dataframe(periods = 2, freq = 'Y')

forecast_years = m.predict(future_years)
forecast_years[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
print(forecast_years)

fig1 = m.plot(forecast_years)
fig2 = m.plot_components(forecast_years)

#comparison with the real fifth year
from fbprophet.diagnostics import cross_validation
df_cv = cross_validation(m, horizon = 5, period = '365,25 days')
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
    #for ...
    #prophet
predictions_2019.append([lat, long, forecast_years["yhat"][5], forecast_years["yhat_lower"][5],forecast_years["yhat_upper"][5], df_p["rmse"][0]])
df_pred = pd.DataFrame(predictions_2019, columns=['lat', 'long', 'mean_price_predicted', 'mean_price_predicted_lower', 'mean_price_predicted_upper', 'rmse'])
print(df_pred)

plt.show()