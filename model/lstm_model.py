from model.base import ModelPredictService, ModelLoader, Model, ModelBuilder
from model.train_data import TrainDataProvider
from constants import windowSize, lstm_units, candel_columns
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense


class LSTMModel(Model):
    def __init__(self, features, coin):
        super().__init__("LSTM", features, coin)


class LSTMModelLoader(ModelLoader):
    def loadModel(self):
        # load model here
        print("LSTMModelLoader model loaded")
        raise NotImplementedError("Subclasses must implement abstract method")


class LSTMModelBuilder(ModelBuilder):
    def __init__(self, model: Model):
        super().__init__(LSTMModel(model.features, model.coin))
        self.dataProvider = TrainDataProvider(
            coin=model.coin, features=model.features, windowSize=windowSize
        )

    def buildModel(self):
        x_train, y_train = self.dataProvider.getTrainData()
        model = Sequential()
        model.add(
            LSTM(
                units=lstm_units,
                return_sequences=True,
                input_shape=(x_train.shape[1], x_train.shape[2]),
            )
        )
        model.add(LSTM(units=lstm_units))
        model.add(Dense(units=len(candel_columns)))
        model.compile(optimizer="adam", loss="mean_squared_error")
        model.fit(x_train, y_train, epochs=1, batch_size=1, verbose=2)
        model.save(self.getModelFileName())


class LSTMModelPredictService(ModelPredictService):
    def __init__(self, model: Model):
        super().__init__(LSTMModel(model.features, model.coin))

    def predict(self, data):
        model = LSTMModelLoader(self.model).loadModel()
        print(f"Predicting with LSTMModel on data: {data}")
        raise NotImplementedError("Subclasses must implement abstract method")
