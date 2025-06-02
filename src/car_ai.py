from sklearn.tree import DecisionTreeClassifier
import numpy as np
import pandas as pd



class DecisionTreeWrapper:

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

    def make_model(self) -> DecisionTreeClassifier:
        model = DecisionTreeClassifier(criterion = "gini")
        model.fit(self.get_features(), self.get_target())
        return model

