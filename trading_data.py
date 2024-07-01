import yfinance as yf
from datetime import date, timedelta


def getTradeData(coin, start_date, end_date):
  data = yf.download(coin, start_date, end_date)
  return data

def getTradeDataToNow(coin, days):
  end_date = date.today()
  start_date = end_date - timedelta(days)
  data = getTradeData(coin, start_date, end_date)

  return data


