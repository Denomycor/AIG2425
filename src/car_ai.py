from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

import numpy as np
import pandas as pd
from sklearn.utils import class_weight


class SKWrapper:

    def __init__(self, file):
        self.df_file = pd.read_csv(file, sep=",")
        self.features = self.get_features()
        self.targets = self.get_target()
        self.preprocess()
        self.train_test_split()

    def feature_names(self):
        return self.df_file.columns[:-1]

    def target_name(self):
        return self.df_file.columns[-1]

    def get_features(self):
        return self.df_file[self.feature_names()]

    def get_target(self):
        return self.df_file["action"]

    def preprocess(self):
        pass

    def train_test_split(self):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.features, self.targets, 
            test_size=0.1,
        )

    def evaluate(self, model):
        y_pred = model.predict(self.X_test)
        print("Accuracy:", accuracy_score(self.y_test, y_pred))
        print("\nClassification Report:\n", classification_report(self.y_test, y_pred, zero_division=0))
        print("Confusion Matrix:\n", confusion_matrix(self.y_test, y_pred))


class DecisionTreeWrapper(SKWrapper):

    def make_model(self) -> DecisionTreeClassifier:
        model = DecisionTreeClassifier(criterion = "gini")
        model.fit(self.X_train, self.y_train)
        return model


class SKNeuralNetwork(SKWrapper):

    def preprocess(self):
        X = self.features.to_numpy()
        X_real = X[:, :-9]
        X_real[X_real < 0] = 150 # If we find negative values representing no collision, make it collide at max dist
        X_bool = X[:, -9:]
        X_real_scaled = X_real / 150 # We use 150 has the reach for sensors
        self.features = np.hstack([X_real_scaled, X_bool])


    def make_model(self) -> MLPClassifier:
        model = MLPClassifier(
            hidden_layer_sizes=(32, 32),
            activation="relu",
            solver='sgd',
            max_iter=1000,
            shuffle=True,
        )

        model.fit(self.X_train, self.y_train)
        return model


class SVMWrapper(SKWrapper):

    def preprocess(self):
        X = self.features.to_numpy()
        X_real = X[:, :-9]
        X_real[X_real < 0] = 150 # If we find negative values representing no collision, make it collide at max dist
        X_bool = X[:, -9:]
        X_real_scaled = X_real / 150 # We use 150 has the reach for sensors
        self.features = np.hstack([X_real_scaled, X_bool])


    def make_model(self) -> SVC:
        model = SVC(kernel='rbf', C=1.0, gamma='scale', class_weight='balanced')
                
        model.fit(self.X_train, self.y_train)
        return model


class KNNWrapper(SKWrapper):

    def preprocess(self):
        X = self.features.to_numpy()
        X_real = X[:, :-9]
        X_real[X_real < 0] = 150 # If we find negative values representing no collision, make it collide at max dist
        X_bool = X[:, -9:]
        X_real_scaled = X_real / 150 # We use 150 has the reach for sensors
        self.features = np.hstack([X_real_scaled, X_bool])


    def make_model(self) -> KNeighborsClassifier:
        model = KNeighborsClassifier(n_neighbors=5)
                
        model.fit(self.X_train, self.y_train)
        return model

