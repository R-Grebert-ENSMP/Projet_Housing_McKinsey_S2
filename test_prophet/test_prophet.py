import pandas as pd
from fbprophet import Prophet

#df = pd.read_csv('.../master_table.csv')
#df = pd.read_csv('Projet_Housing_McKinsey_S2/test_prophet/test_years.csv')
data = {'ds' : [2014, 2015, 2016, 2017, 2018], 'y' : [1000, 2000, 3000, 4000, 5000]}
df = pd.DataFrame(data, columns = ['ds', 'y'])
print(df)

m = Prophet()
m.fit(df)
future_years = m.make_future_dataframe(periods = 1, freq = 'year')
future_years.tail()
#forecast_years = m.predict(future_years)

#forecast_years[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

#comparison with the real fifth year
from fbprophet.diagnostics import cross_validation
#df_cv = m.cross_validation(horizon = 1, unit = 'years', initial = 4)
df_cv.head()
