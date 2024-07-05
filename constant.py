# getAllDataToCSV()
algorithms = [
    {"label": "LSTM", "value": "lstm"},
    {"label": "RNN", "value": "rnn"},
    {"label": "XGBoost", "value": "xgboost"},
]

coin_labels = [
    {"label": "BTC-USD", "value": "btcusd"},
    {"label": "ETH-USD", "value": "ethusd"},
    {"label": "XRP-USD", "value": "xrpusd"},
    {"label": "LTC-USD", "value": "ltcusd"},
    {"label": "ADA-USD", "value": "adausd"},
    {"label": "DOT-USD", "value": "dotusd"},
    {"label": "SOL-USD", "value": "solusd"},
    {"label": "LINK-USD", "value": "linkusd"},
    {"label": "MATIC-USD", "value": "maticusd"},
    {"label": "DOGE-USD", "value": "dogeusd"},
]
day_number = [10, 20, 30, 60, 120]
timeframes = {
    "day": {
        "label": "1 ngày",
        "value": 86400,
    },
    "hour": {
        "label": "1 giờ",
        "value": 3600,
    },
    "minute": {
        "label": "1 phút",
        "value": 60,
    },
}
# timeframes = [
#     {"label": "1 phút", "value": 60},
#     {"label": "1 tiếng", "value": 3600},
#     {"label": "1 ngày", "value": 86400},
# ]
features = ["close", "ROC"]
windowSize = 50
models = ["LSTM", "RNN", "XGB"]
coins = [
    "btcusd",
    # "ethusd",
    # "adausd",
]
candel_columns = ["open", "high", "low", "close"]
lstm_units = 50
simple_rnn_units = 50