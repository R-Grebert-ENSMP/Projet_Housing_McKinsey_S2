import pandas as pd
from fbprophet import Prophet

#df = pd.read_csv('.../master_table.csv')
df = pd.read_csv('Projet_Housing_McKinsey_S2/test_prophet/test_years.csv')

Prophet.fit(df)
future_years = Prophet.make_future_dataframe(periods = 1, freq = 'year')
forecast_years = Prophet.predict(future_years)

forecast_years[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

#comparison with the real fifth year
from fbprophet.diagnostics import cross_validation
df_cv = Prophet.cross_validation(horizon = 1, unit = 'years', initial = 4)
df_cv.head()
