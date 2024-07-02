from constants import features as validFeatures, coins, windowSize
import pandas as pd
from model.train_data import TrainDataProvider
from model.utils import CoinValidator, FeatureValidator

class Model:
    def __init__(self, modelName, features, coin):
        self.modelName = modelName
        # check if features are valid
        if not FeatureValidator().areValidFeatures(features):
            raise ValueError(f"Invalid features: {features}")
        self.features = features

        if not CoinValidator().isValidCoin(coin):
            raise ValueError(f"Invalid coin: {coin}")
        self.coin = coin


class ModelInputExtractor:
    def __init__(self, model: Model):
        self.model = model

    def extractData(self, data):
        return data[self.model.features]


class ModelInputValidator:
    def __init__(self, model: Model):
        self.model = model

    def isValidInput(self, data):
        assert isinstance(data, pd.DataFrame)
        return FeatureValidator(self.model.features).areValidFeatures(data.columns)


class ModelLoader:
    def __init__(self, model: Model):
        self.model = model

    def loadModel(self):
        raise NotImplementedError("Subclasses must implement abstract method")


class ModelPredictService:
    def __init__(self, model: Model):
        self.model = model
        self.inputExtractor = ModelInputExtractor(model)
        self.inputValidator = ModelInputValidator(model)
        self.scaler = TrainDataProvider(
            coin=model.coin, features=model.features, windowSize=windowSize
        ).scaler

    def predict(self, data: pd.DataFrame) -> pd.DataFrame:
        print(f"Predicting with {self.model.modelName} on data: {data}")
        raise NotImplementedError("Subclasses must implement abstract method")

    def execute(self, data):
        if not self.inputValidator.isValidInput(data):
            raise ValueError("Invalid input")
        data = self.inputExtractor.extractData(data)
        data = self.scaler.scale(data)
        x_data = data.values.reshape(1, data.shape[0], data.shape[1])
        df_prediction = self.predict(x_data)
        inverseScaled_output_data = self.scaler.inverseScale(df_prediction)
        return inverseScaled_output_data
    
class SavedModelPredictService(ModelPredictService):
    def __init__(self, model: Model, modelLoader: ModelLoader):
        super().__init__(model)
        self.modelLoader = modelLoader

    def predictWithLoadedModel(self, loaded_model, data: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError("Subclasses must implement abstract method")

    def predict(self, data: pd.DataFrame):
        loaded_model = self.modelLoader.loadModel()
        return self.predictWithLoadedModel(loaded_model, data)

class ModelFileService:
    def __init__(self, model: Model):
        self.model = model

    @staticmethod
    def getModelFileDirectory():
        return "./model/built_models"

    def getModelFileName(self):
        return f"./model/built_models/{self.model.modelName}_{self.model.coin}_{'_'.join(self.model.features)}.keras"


class ModelBuilder:
    def __init__(self, model: Model):
        self.model = model
        self.modelFileService = ModelFileService(model=model)

    def buildModel(self):
        raise NotImplementedError("Subclasses must implement abstract method")