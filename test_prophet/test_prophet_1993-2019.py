import pandas as pd
from fbprophet import Prophet
import datetime
import matplotlib.pyplot as plt

days2014 = [datetime.date(2014,i,j) for i in range(1,13) for j in range(1,29)]
days2015 = [datetime.date(2015,i,j) for i in range(1,13) for j in range(1,29)]
days2016 = [datetime.date(2016,i,j) for i in range(1,13) for j in range(1,29)]
days2017 = [datetime.date(2017,i,j) for i in range(1,13) for j in range(1,29)]
days2018 = [datetime.date(2018,i,j) for i in range(1,13) for j in range(1,29)]

#df = pd.read_csv('.../master_table.csv') 
#df = pd.read_csv('Projet_Housing_McKinsey_S2/test_prophet/test_years.csv')
#data = {'ds' : days2014+days2015+days2016+days2017+days2018, 'y' : [1000+k*300/(12*28) for k in range(12*28)]+[1300+k*150/(12*28) for k in range(12*28)]+[1400-k*250/(12*28) for k in range(12*28)]+[1150+k*50/(12*28) for k in range(12*28)] + [1200+k*300/(12*28) for k in range(12*28)]}
data = {'ds' : [datetime.date(2014, 1, 1), datetime.date(2015, 1, 1), datetime.date(2016, 1, 1), datetime.date(2017, 1, 1), datetime.date(2018, 1, 1)], 'y' : [1000, 2000, 1500, 3000, 3300], 'voisin droite' : [1100, 2200, 1600, 3300, 3100], 'voisin gauche' : [1000, 1900, 1500, 3000, 3100], 'voisin haut' : [900, 1900, 1600, 2900, 3000], 'voisin bas' : [1000, 2000, 1400, 3000, 3200]}
df = pd.DataFrame(data, columns = ['ds', 'y', 'voisin droite', 'voisin gauche', 'voisin haut', 'voisin bas'])
df['floor']=0
df['cap']=10000
print(df)


m = Prophet(growth='logistic')
m.add_regressor('voisin droite')
m.add_regressor('voisin gauche')
m.add_regressor('voisin haut')
m.add_regressor('voisin bas')
m.fit(df)
future_years = m.make_future_dataframe(periods = 3, freq = 'Y')
future_years['voisin droite'] = [1100, 2200, 1600, 3300, 3100, 3500, 3600, 3200]
future_years['voisin gauche'] = [1000, 1900, 1500, 3000, 3100, 3400, 3700, 3300]
future_years['voisin haut'] = [900, 1900, 1600, 2900, 3000, 3500, 3500, 3300]
future_years['voisin bas'] = [1000, 2000, 1400, 3000, 3200, 3400, 3600, 3400]
#future_years = m.make_future_dataframe(periods=3*365)
future_years['floor']=0
future_years['cap']=10000


forecast_years = m.predict(future_years)
forecast_years[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
print(forecast_years)
fig1 = m.plot(forecast_years)
fig2 = m.plot_components(forecast_years)


#comparison with the real fifth year
#from fbprophet.diagnostics import cross_validation
#df_cv = cross_validation(m, horizon = 365, initial = 4*365)
#df_cv.head()

plt.show()