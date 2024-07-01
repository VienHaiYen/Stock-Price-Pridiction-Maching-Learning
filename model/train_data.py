from sklearn.preprocessing import MinMaxScaler
from model.base import FeatureValidator, CoinValidator
import pandas as pd
from constants import candel_columns
import numpy as np


class ROCCalculator:
    def fromClose(self, close):
        assert isinstance(close, pd.Series)
        return ((close - close.shift(1)) / close.shift(1)).fillna(0)


class TrainDataProvider:
    def __init__(self, coin, features, windowSize):
        # check if coin is valid
        if not CoinValidator().isValidCoin(coin):
            raise ValueError(f"Invalid coin: {coin}")
        self.coin = coin
        # check if features are valid
        if not FeatureValidator().areValidFeatures(features):
            raise ValueError(f"Invalid features: {features}")
        self.features = features
        self.windowSize = windowSize

    def getDataFromFile(self):
        data = pd.read_csv(f"./data/{self.coin}.csv")
        data["Date"] = pd.to_datetime(data["Date"])
        data.index = data["Date"]
        data = data.drop(["Date"], axis=1)
        data.sort_index(ascending=True, axis=0, inplace=True)
        return data
    
    def extractData(self, data: pd.DataFrame):
        return data[[*self.features, *candel_columns]]

    def getXYData(self, data: pd.DataFrame):
        x_data = data[self.features].values
        y_data = data[candel_columns].values
        return x_data, y_data

    def scaleData(self, data: pd.DataFrame):
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(data)
        return pd.DataFrame(scaled_data, columns=data.columns)
        

    def getTrainDataset(self, x_data, y_data, windowSize):
        assert x_data.ndim == 2
        assert isinstance(x_data, np.ndarray)
        assert len(x_data) == len(y_data)

        num_features = x_data.shape[1]
        X = np.lib.stride_tricks.sliding_window_view(
            x_data[:-1, :], window_shape=(windowSize, num_features), axis=(0, 1)
        )
        X = X.reshape(-1, windowSize, num_features)
        Y = y_data[windowSize:, :]

        return X, Y

    def getTrainData(self):
        # get data
        data = self.getDataFromFile()
        data["ROC"] = ROCCalculator().fromClose(data["Close"])
        extracted_data = self.extractData(data)
        scaled_data = self.scaleData(extracted_data)
        x_data, y_data = self.getXYData(scaled_data)
        x_train, y_train = self.getTrainDataset(x_data, y_data, self.windowSize)

        return x_train, y_train
