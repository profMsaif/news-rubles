import numpy as np 
import pandas as pd
import math
import datetime
from datetime import datetime as dt
import yfinance as yf
# visualizations
import matplotlib.pyplot as plt
import seaborn as sns
from fbprophet.diagnostics import cross_validation
from fbprophet.plot import plot_cross_validation_metric
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go
# time series algorithm
from fbprophet import Prophet
from fbprophet.diagnostics import performance_metrics
from fbprophet.diagnostics import cross_validation

class Model_Prophet:

   def get_data():
      data_usdrub = yf.download('USDRUB=X', start='2017-01-01', end=datetime.datetime.now().date())
      data_eurub = yf.download('EURRUB=X', start='2017-01-01', end=datetime.datetime.now().date())
      return data_usdrub,data_eurub

   def ml_model(df):
      df_columns = ['ds','y']
      train_columns = ['Close']
      train = df[train_columns]
      train = train.rename(columns={'Close':'y'})
      train.index.names =['ds']
      train =train.reset_index()
      df = df.rename(columns={'Close':'y'})
      df.index.names =['ds']
      df =train.reset_index()
      
      m = Prophet(daily_seasonality=False,yearly_seasonality=True,
               weekly_seasonality= True,changepoint_prior_scale= 0.05, 
               seasonality_prior_scale= 20.0, holidays_prior_scale= 5.0)
      m.fit(train)
      
      future = m.make_future_dataframe(periods=30)
      forecast = m.predict(future)
      
      cmp_df = forecast.set_index('ds')[['yhat', 'yhat_lower', 'yhat_upper']].join(df[df_columns].set_index('ds'))
      cmp_df['e'] = cmp_df['y'] - cmp_df['yhat']
      mae=np.mean(abs(cmp_df[-45:-15]['e']))
      
      forecast = forecast[['ds','yhat_lower']][-30:]
      forecast['yhat_lower'] = forecast['yhat_lower'].apply(lambda x:x-mae)
      return forecast

   def get_forecast(self, df):
      forecast = self.ml_model(df)
      forecast = forecast[['ds','yhat_lower']][-30:]
      return forecast

   def ml_predict(self, usd=True,eur=True):
      df_usdrub,df_eurub=self.get_data()
      if usd==True:
         forecast_usdrub = self.get_forecast(df_usdrub)
         return forecast_usdrub
      if eur==True:
         forecast_eurub = self.get_forecast(df_eurub)
         return forecast_eurub

