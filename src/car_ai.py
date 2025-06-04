from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier

import numpy as np
import pandas as pd


class SKWrapper:

    def __init__(self, file):
        self.df_file = pd.read_csv(file, sep=",")

    def feature_names(self):
        return self.df_file.columns[:-1]

    def target_name(self):
        return self.df_file.columns[-1]

    def get_features(self):
        return self.df_file[self.feature_names()]

    def get_target(self):
        return self.df_file["action"]

class DecisionTreeWrapper(SKWrapper):

    def make_model(self) -> DecisionTreeClassifier:
        model = DecisionTreeClassifier(criterion = "gini")
        model.fit(self.get_features(), self.get_target())
        return model


class SKNeuralNetwork(SKWrapper):
    
    def make_model(self) -> MLPClassifier:
        model = MLPClassifier(
            hidden_layer_sizes=(32, 32),
            activation="relu",
            solver='sgd',
            max_iter=1000,
            shuffle=True
        )
        X = self.get_features().to_numpy()
        X_real = X[:, :-9]
        X_real[X_real < 0] = 150 # If we find negative values representing no collision, make it collide at max dist
        X_bool = X[:, -9:]

        X_real_scaled = X_real / 150 # We use 150 has the reach for sensors

        X_scaled = np.hstack([X_real_scaled, X_bool])
        print(X_scaled[10])

        model.fit(X_scaled, self.get_target())
        return model

