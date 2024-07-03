from model.base import (
    Model,
    ModelBuilder,
    SavedModelPredictService,
    XGBModelInputValidator,
    XGBModelFileService,
)
from model.train_data import TrainDataProvider
from model.loader import XGBModelLoader
from constants import candel_columns
import pandas as pd
from xgboost import XGBRegressor


class XGBModel(Model):
    def __init__(self, features, coin):
        super().__init__("XGBoost", features, coin)


class XGBModelBuilder(ModelBuilder):
    def __init__(self, model: Model):
        xgbModel = XGBModel(model.features, model.coin)
        super().__init__(
            model=xgbModel,
            modelFileService=XGBModelFileService(model=xgbModel),
        )
        self.dataProvider = TrainDataProvider(coin=model.coin, features=model.features)

    def buildModel(self):
        x_train, y_train = self.dataProvider.getTrainData()

        model = XGBRegressor(learning_rate=0.1, n_estimators=100, max_depth=5)
        model.fit(x_train, y_train)
        model.save_model(self.modelFileService.getModelFileName())


class XGBModelPredictService(SavedModelPredictService):
    def __init__(self, model: XGBModel):
        super().__init__(
            model=model,
            modelLoader=XGBModelLoader(model),
            inputValidator=XGBModelInputValidator(model),
        )

    def predictWithLoadedModel(self, loaded_model, data: pd.DataFrame) -> pd.DataFrame:
        # data shape (1, n_features)
        data = data.values
        prediction = loaded_model.predict(data)  # (1, 4)
        df_prediction = pd.DataFrame(prediction, columns=candel_columns)
        return df_prediction
