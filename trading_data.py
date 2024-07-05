import requests
import pandas as pd

def getDataFromCoin(coin, timeframe, day_number):
  url = f"https://www.bitstamp.net/api/v2/ohlc/{coin}/"
  params = {
          "step":timeframe,
          "limit":int(day_number),
          }
  df = requests.get(url, params=params).json()["data"]["ohlc"]

  df = pd.DataFrame(df)
  df.timestamp = pd.to_datetime(df.timestamp, unit = "s")
  return df

def getDataFromCoinToCSV(coin):
  url = f"https://www.bitstamp.net/api/v2/ohlc/{coin}/"
  params = {
          "step":86400,
          "limit":int(365*5),
          }
  df = requests.get(url, params=params).json()["data"]["ohlc"]
  df = pd.DataFrame(df)
  df.timestamp = pd.to_datetime(df.timestamp, unit = "s")
  new_df = df[['timestamp', 'open', 'close', 'high', 'low']]

  new_df.to_csv(f'./data/{coin}.csv')

def getAllDataToCSV():
  coins = [
    'btcusd', 'ethusd', 'xrpusd', 'ltcusd', 'adausd', 'dotusd', 'solusd', 'linkusd', 'maticusd', 'dogeusd', ]
  for coin in coins:
    getDataFromCoinToCSV(coin)

getAllDataToCSV()