import pandas as pd
from fbprophet import Prophet
import datetime
import matplotlib.pyplot as plt


data = {'ds' : [datetime.date(k, 1, 1) for k in range(2014, 2020)], 'y' : [8000, 8100, 8900, 9500, 10200, 10500]}
df = pd.DataFrame(data, columns = ['ds', 'y'])

m = Prophet()
m.fit(df)
future_years = m.make_future_dataframe(periods = 2, freq = 'Y')

forecast_years = m.predict(future_years)
forecast_years[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

fig1 = m.plot(forecast_years)
fig2 = m.plot_components(forecast_years)

#comparison with the real fifth year
from fbprophet.diagnostics import cross_validation
df_cv = cross_validation(m, horizon = 6, period = '365,25 days')
print(df_cv.head())

#prediction model evalution
from fbprophet.diagnostics import performance_metrics
df_p = performance_metrics(df_cv)
print(df_p.head())

plt.show()