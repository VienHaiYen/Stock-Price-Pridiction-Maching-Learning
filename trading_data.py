import requests
import pandas as pd
import pandas_ta as ta

def getDataFromCoin(coin):
  url = f"https://www.bitstamp.net/api/v2/ohlc/{coin}/"
  params = {
          "step":86400,
          "limit":int(365),
          }
  df = requests.get(url, params=params).json()["data"]["ohlc"]
  df = pd.DataFrame(df)
  df.timestamp = pd.to_datetime(df.timestamp, unit = "s")

  df["rsi"] = ta.rsi(df.close.astype(float))
  print(coin)
  print(df.head())
  df.to_csv(f'./data/{coin}.csv')

coins = [
  'btcusd', 'ethusd', 'xrpusd', 'ltcusd', 'bnbusd', 'adausd', 'dotusd', 'solusd', 'linkusd', 'maticusd', 'dogeusd', ]
for coin in coins:
  getDataFromCoin(coin)
