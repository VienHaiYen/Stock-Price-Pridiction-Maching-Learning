from model.base import ModelLoader, Model, ModelFileService
from tensorflow.keras.models import load_model
from xgboost import XGBRegressor

class KerasModelLoader(ModelLoader):
    def __init__(self, model: Model):
        super().__init__(model)
        self.modelFileService = ModelFileService(self.model)

    def loadModel(self):
        filePath = self.modelFileService.getModelFileName()
        return load_model(filePath)
class XGBModelLoader(ModelLoader):
    def __init__(self, model: Model):
        super().__init__(model)
        self.modelFileService = ModelFileService(self.model)

    def loadModel(self):
        filePath = self.modelFileService.getModelFileName()
        model = XGBRegressor()
        model.load_model(filePath)
        return model