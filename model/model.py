class Model:
    def __init__(self, model_name):
        self.model_name = model_name

    def predict(self, data):
        print(f"Predicting with {self.model_name} on data: {data}")
class XGBoostModel(Model):
    def __init__(self):
        super().__init__("XGBoost")

    def predict(self, data):
        print(f"Predicting with {self.model_name} on data: {data}")
class RNNModel(Model):
    def __init__(self):
        super().__init__("RNN")

    def predict(self, data):
        print(f"Predicting with {self.model_name} on data: {data}")
class LSTMModel(Model):
    def __init__(self):
        super().__init__("LSTM")

    def predict(self, data):
        print(f"Predicting with {self.model_name} on data: {data}")