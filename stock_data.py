import yfinance as yf
from datetime import date, timedelta


def getStockData(stock, start_date, end_date):
  # get data
  yf_clone = yf
  data = yf_clone.download(stock, start_date, end_date)
  return data


def getStockDataToNow(stock, days):
  end_date = date.today()
  start_date = end_date - timedelta(days)
  data = getStockData(stock, start_date, end_date)

  return data


def getAllDataToCSV():
  coins = [
      "BTC-USD",
      "ETH-USD",
      #  "BNB-USD", "ADA-USD", "XRP-USD",
      #  "SOL-USD", "DOT-USD", "DOGE-USD", "SHIB-USD", "LTC-USD"
  ]

  for coin in coins:
      data = getStockDataToNow(coin, 5 * 365)
      data.to_csv(f"./data/{coin}.csv")
