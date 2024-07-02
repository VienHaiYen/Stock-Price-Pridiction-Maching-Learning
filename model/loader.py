from model.base import ModelLoader, Model, ModelFileService
from tensorflow.keras.models import load_model

class KerasModelLoader(ModelLoader):
    def __init__(self, model: Model):
        super().__init__(model)
        self.modelFileService = ModelFileService(self.model)

    def loadModel(self):
        filePath = self.modelFileService.getModelFileName()
        return load_model(filePath)