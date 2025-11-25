"""
ML model wrapper: scaling, window creation, model training,
and prediction.
"""

import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout


class ModelInference:
    def __init__(self, look_back=100, neurons=50):
        self.look_back = look_back
        self.neurons = neurons
        self.scaler = MinMaxScaler(feature_range=(-1, 1))

    def scale(self, data):
        scaled = self.scaler.fit_transform(data)
        return scaled

    def create_windows(self, data):
        X, y = [], []
        for i in range(self.look_back, len(data)):
            X.append(data[i - self.look_back:i])
            y.append(data[i])
        return np.array(X), np.array(y)

    def build_model(self, input_shape):
        model = Sequential([
            LSTM(self.neurons, input_shape=input_shape, return_sequences=True),
            Dropout(0.2),
            LSTM(self.neurons),
            Dense(1),
        ])
        model.compile(loss="mse", optimizer="adam")
        return model
