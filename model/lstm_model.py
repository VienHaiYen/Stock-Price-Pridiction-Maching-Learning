from model.base import (
    ModelPredictService,
    ModelLoader,
    Model,
    ModelBuilder,
    ModelFileService,
)
from model.train_data import TrainDataProvider, DataScaler
from constants import windowSize, lstm_units, candel_columns
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Input
import pandas as pd


class LSTMModel(Model):
    def __init__(self, features, coin):
        super().__init__("LSTM", features, coin)


class LSTMModelLoader(ModelLoader):
    def __init__(self, model: Model):
        lstmModel = LSTMModel(model.features, model.coin)
        super().__init__(lstmModel)
        self.modelFileService = ModelFileService()

    def loadModel(self):
        filePath = self.modelFileService.getModelFileName(self.model)
        return load_model(filePath)


class LSTMModelBuilder(ModelBuilder):
    def __init__(self, model: Model):
        super().__init__(LSTMModel(model.features, model.coin))
        self.dataProvider = TrainDataProvider(
            coin=model.coin, features=model.features, windowSize=windowSize
        )

    def buildModel(self):
        x_train, y_train = self.dataProvider.getTrainData()
        inputShape = (x_train.shape[1], x_train.shape[2])

        model = Sequential()
        model.add(Input(shape=inputShape))
        model.add(
            LSTM(
                units=lstm_units,
                return_sequences=True,
            )
        )
        model.add(LSTM(units=lstm_units))
        model.add(Dense(units=y_train.shape[1]))
        model.compile(optimizer="adam", loss="mean_squared_error")
        model.fit(x_train, y_train, epochs=1, batch_size=1, verbose=2)
        model.save(self.getModelFileName())


class LSTMModelPredictService(ModelPredictService):
    def __init__(self, model: LSTMModel):
        super().__init__(model, LSTMModelLoader(model))
        dataProvider = TrainDataProvider(
            coin=model.coin, features=model.features, windowSize=windowSize
        )
        self.scaler = DataScaler(data=dataProvider.getDataFromFile())

    def predict(self,loaded_model, data: pd.DataFrame):
        data = self.scaler.scale(data)
        x_data = data.values.reshape(1, data.shape[0], data.shape[1])
        prediction = loaded_model.predict(x_data) # shape (1, 4)
        df_prediction = pd.DataFrame(prediction, columns=candel_columns)
        return self.scaler.inverseScale(df_prediction)
