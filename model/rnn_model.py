from model.base import Model, ModelBuilder, SavedModelPredictService
from model.train_data import TrainDataProvider
from model.loader import KerasModelLoader
from constants import windowSize, simple_rnn_units, candel_columns
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, Dense, Input

class RNNModel(Model):
    def __init__(self, features, coin):
        super().__init__("RNN", features, coin)


class RNNModelBuilder(ModelBuilder):
    def __init__(self, model: Model):
        super().__init__(RNNModel(model.features, model.coin))
        self.dataProvider = TrainDataProvider(
            coin=model.coin, features=model.features, windowSize=windowSize
        )

    def buildModel(self):
        x_train, y_train = self.dataProvider.getTrainData()
        inputShape = (x_train.shape[1], x_train.shape[2])

        model = Sequential()
        model.add(Input(shape=inputShape))
        model.add(
            SimpleRNN(
                units=simple_rnn_units,
                return_sequences=True,
            )
        )
        model.add(SimpleRNN(units=simple_rnn_units))
        model.add(Dense(units=y_train.shape[1]))
        model.compile(optimizer="adam", loss="mean_squared_error")
        model.fit(x_train, y_train, epochs=1, batch_size=1, verbose=2)
        model.save(self.modelFileService.getModelFileName())
    
class RNNModelPredictService(SavedModelPredictService):
    def __init__(self, model: RNNModel):
        super().__init__(model, KerasModelLoader(model))

    def predictWithLoadedModel(self, loaded_model, data: pd.DataFrame):
        prediction = loaded_model.predict(data)
        df_prediction = pd.DataFrame(prediction, columns=candel_columns)
        return df_prediction
