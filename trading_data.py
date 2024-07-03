import yfinance as yf
from datetime import date, timedelta
import pandas as pd


def getTradeData(coin, start_date, end_date):
  data = yf.download(coin, start_date, end_date)
  return data

def getTradeDataToNow(coin, days):
  end_date = date.today()
  start_date = end_date - timedelta(days)
  data = getTradeData(coin, start_date, end_date)

  return data

def getTradeDataByMinute(coin):
  data = yf.download(coin, start= date.today(), interval='1m')
  # real_time = data.iloc[-1:].copy()

  # print(data)
  # data.to_csv('test11.csv')

  open = data['Open'][0]
  high = data['High'].max()
  low = data['Low'].min()
  close = data['Close'][-1]
  adj_close = data['Adj Close'][-1]
  # print(open, high, low, close, adj_close)

  result = pd.DataFrame({
    'Open': open,
    'High': high,
    'Low': low,
    'Close': close,
    'Adj Close': adj_close,
  }, index=[date.today()])
  print(result)

  return result

getTradeDataByMinute('BTC-USD')

# a = getTradeData('BTC-USD', date.today() - timedelta(10), date.today())
# a['Date'] = a.index
# print(a['Date'].max())