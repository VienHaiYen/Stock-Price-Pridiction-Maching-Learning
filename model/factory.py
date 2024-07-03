from model.lstm_model import LSTMModelPredictService, LSTMModel
from model.rnn_model import RNNModelPredictService, RNNModel
from model.xgboost_model import XGBModelPredictService, XGBModel

class ModelPredictServiceFactory:
    @staticmethod
    def getModelPredictService(modelName, features, coin):
        if modelName == "LSTM":
            return LSTMModelPredictService(model=LSTMModel(features=features, coin=coin))
        elif modelName == "RNN":
            return RNNModelPredictService(model=RNNModel(features=features, coin=coin))
        elif modelName == "XGB":
            return XGBModelPredictService(model=XGBModel(features=features, coin=coin))
        else:
            raise Exception("Model not found")