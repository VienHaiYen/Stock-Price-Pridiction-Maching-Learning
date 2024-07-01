import yfinance as yf
from datetime import date, timedelta


def getStockData(stock, start_date, end_date):
  data = yf.download(stock, start_date, end_date)
  return data

def getStockDataToNow(stock, days):
  end_date = date.today()
  start_date = end_date - timedelta(days)
  data = getStockData(stock, start_date, end_date)

  return data


coins = ["BTC-USD", "ETH-USD",
    #  "BNB-USD", "ADA-USD", "XRP-USD",
    #  "SOL-USD", "DOT-USD", "DOGE-USD", "SHIB-USD", "LTC-USD"
      ]
