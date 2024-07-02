from model.lstm_model import LSTMModelBuilder
from model.rnn_model import RNNModelBuilder
from model.xgboost_model import XGBModelBuilder
from model.base import Model, ModelFileService
from constants import coins, features
from itertools import combinations
import os


class ModelsInitializer:
    def __init__(self, features=features, coins=coins):
        self.features = features
        self.coins = coins
        self.models = [LSTMModelBuilder, RNNModelBuilder, XGBModelBuilder]
        self.modelFileDirectory = ModelFileService.getModelFileDirectory()

    def getFeaturesCombination(self):
        results = []
        for num_of_feature in range(1, len(self.features) + 1):
            for feature_combination in combinations(self.features, num_of_feature):
                results.append(list(feature_combination))
        return results

    def clearOldModelFiles(self):
        path = self.modelFileDirectory
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            os.remove(file_path)

    def buildModels(self):
        for coin in self.coins:
            for features_combination in self.getFeaturesCombination():
                for ModelBuilder in self.models:
                    ModelBuilder(
                        model=Model(
                            modelName="", features=features_combination, coin=coin
                        )
                    ).buildModel()

    def init(self):
        self.clearOldModelFiles()
        self.buildModels()
