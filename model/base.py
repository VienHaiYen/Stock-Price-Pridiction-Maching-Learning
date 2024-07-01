from constants import features as validFeatures, coins
import pandas as pd


class CoinValidator:
    def __init__(self, validCoins=coins):
        self.validCoins = validCoins

    def isValidCoin(self, coin):
        return coin in self.validCoins

    def areValidCoins(self, coins):
        return all([self.isValidCoin(coin) for coin in coins])


class FeatureValidator:
    def __init__(self, validFeatures=validFeatures):
        self.validFeatures = validFeatures

    def isValidFeature(self, feature):
        return feature in self.validFeatures

    def areValidFeatures(self, features):
        return all([self.isValidFeature(feature) for feature in features])


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


class ModelPredictService:
    def __init__(self, model: Model):
        self.model = model
        self.inputExtractor = ModelInputExtractor(model)
        self.inputValidator = ModelInputValidator(model)

    def predict(self, data):
        print(f"Predicting with {self.model.modelName} on data: {data}")
        raise NotImplementedError("Subclasses must implement abstract method")

    def execute(self, data):
        if not self.inputValidator.isValidInput(data):
            raise ValueError("Invalid input")
        data = self.inputExtractor.extractData(data)
        return self.predict(data)


class ModelLoader:
    def __init__(self, model: Model):
        self.model = model

    def loadModel(self):
        raise NotImplementedError("Subclasses must implement abstract method")

class ModelFileService:
    def getModelFileDirectory(self):
        return "./model/built_models"

    def getModelFileName(self, model:Model):
        return (
            f"./model/built_models/{model.modelName}_{model.coin}_{'_'.join(model.features)}.keras"
        )

class ModelBuilder:
    def __init__(self, model: Model):
        self.model = model
        self.modelFileService = ModelFileService()

    def getModelFileName(self):
        return self.modelFileService.getModelFileName(self.model)

    def buildModel(self):
        raise NotImplementedError("Subclasses must implement abstract method")