from sklearn.tree import DecisionTreeClassifier
import pandas as pd

import torch
import torch.nn
import torch.nn.functional



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



class NeuralWrapper(torch.nn.Module):
    
    arch = [18,16,16,16]

    def __init__(self):
        super().__init__()
        self.l1 = torch.nn.Linear(self.arch[0],self.arch[1])
        self.l2 = torch.nn.Linear(self.arch[1],self.arch[2])
        self.l3 = torch.nn.Linear(self.arch[2],self.arch[3])


    def forward(self, input: torch.Tensor) -> torch.Tensor:
        a1 = torch.nn.functional.relu(self.l1(input))
        a2 = torch.nn.functional.relu(self.l2(a1))
        out = self.l3(a2)
        return out


    def get_neural_genes(self):
        return self.state_dict()


    def set_neural_genes(self, genes):
        self.load_state_dict(genes, False)


    def predict(self, input_normalized) -> int:
        self.eval()
        input_tensor = torch.tensor(input_normalized)
        output_tensor = self.forward(input_tensor)

        selected_i = 0

        for i in range(self.arch[-1]):
            selected_i = i if output_tensor[i].item() > output_tensor[selected_i].item() else selected_i

        return selected_i

