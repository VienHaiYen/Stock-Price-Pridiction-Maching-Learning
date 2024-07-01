from sklearn.preprocessing import MinMaxScaler
from model.base import FeatureValidator, CoinValidator
import pandas as pd
from constants import candel_columns
import numpy as np


class ROCCalculator:
    def fromClose(self, close):
        assert isinstance(close, pd.Series)
        return ((close - close.shift(1)) / close.shift(1)).fillna(0)


class DataScaler:
    def __init__(self, data: pd.DataFrame):
        scaler = MinMaxScaler(feature_range=(0, 1))
        self.scaler = scaler.fit(data)
        self.df_mean = data.mean()

    def fillMissingColumns(self, data: pd.DataFrame):
        copied_data = data.copy()
        missing_columns = set(self.scaler.feature_names_in_) - set(copied_data.columns)
        for column in missing_columns:
            copied_data[column] = self.df_mean[column]
        reordered_data = copied_data[self.scaler.feature_names_in_]
        return reordered_data

    def scale(self, data: pd.DataFrame):
        filled_data = self.fillMissingColumns(data)
        scaled_data = self.scaler.transform(filled_data)

        df_scaled = pd.DataFrame(scaled_data, columns=filled_data.columns)
        return df_scaled[data.columns]

    def inverseScale(self, data: pd.DataFrame):
        filled_data = self.fillMissingColumns(data)
        inverse_scaled_data = self.scaler.inverse_transform(filled_data)

        df_inverse_scaled = pd.DataFrame(
            inverse_scaled_data, columns=filled_data.columns
        )
        return df_inverse_scaled[data.columns]


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

    def getRawDataFromFile(self):
        data = pd.read_csv(f"./data/{self.coin}.csv")
        data["Date"] = pd.to_datetime(data["Date"])
        data.index = data["Date"]
        data = data.drop(["Date"], axis=1)
        data.sort_index(ascending=True, axis=0, inplace=True)
        return data

    def extractData(self, data: pd.DataFrame):
        return data[list(set([*self.features, *candel_columns]))]

    def getDataFromFile(self) -> pd.DataFrame:
        data = self.getRawDataFromFile()
        data["ROC"] = ROCCalculator().fromClose(data["Close"])
        extracted_data = self.extractData(data)
        return extracted_data
    
    def getXYData(self, data: pd.DataFrame):
        x_data = data[self.features].values
        y_data = data[candel_columns].values
        return x_data, y_data

    def scaleData(self, data: pd.DataFrame):
        scaler = DataScaler(data=data)
        scaled_data = scaler.scale(data)
        return scaled_data

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
        scaled_data = self.scaleData(data)
        x_data, y_data = self.getXYData(scaled_data)
        x_train, y_train = self.getTrainDataset(x_data, y_data, self.windowSize)

        return x_train, y_train