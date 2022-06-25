import numpy as np
import datetime
import yfinance as yf
from prophet import Prophet
from mainpage import models
from dataclasses import dataclass

@dataclass
class Predict:
   forecast: float
   timestamp: str
   id_currency: int

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
      forecast['yhat_lower'] = forecast['yhat_lower'].apply(lambda x:x-0.9*mae)
      return forecast

   def get_forecast(df, self):
      forecast = self.ml_model(df)
      forecast = float(forecast[['yhat_lower']][-30:-29].iloc[0])
      return forecast

   def ml_predict(self, usd=True,eur=True):
      df_usdrub,df_eurub = self.get_data()
      if usd == True:
         forecast_usdrub = self.get_forecast(df_usdrub)
         return forecast_usdrub
      if eur==True:
         forecast_eurub = self.get_forecast(df_eurub)
         return forecast_eurub

   def save_to_table(self, usd=True):
      
      predict = self.ml_predict(usd=usd)

      valute = models.Currency.objects.get(name='USD') if usd == True else models.Currency.objects.get(name='EUR')

      mdl = Predict(
         forecast = predict,
         timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
         id_currency = valute.id
      )

      model = models.Forecast.objects.create(mdl)
      model.save()
      return model



