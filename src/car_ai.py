from sklearn.tree import DecisionTreeClassifier
import numpy as np
import pandas as pd

from sklearn.utils.class_weight import compute_class_weight

from torch.utils.data import Dataset
import torch
import torch.nn
import torch.nn.functional
import torch.optim



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

    def __init__(self, file):
        super().__init__()
        self.dataset = TorchDataset(file)
        self.l1 = torch.nn.Linear(self.arch[0],self.arch[1])
        self.l2 = torch.nn.Linear(self.arch[1],self.arch[2])
        self.l3 = torch.nn.Linear(self.arch[2],self.arch[3])


    def forward(self, input: torch.Tensor) -> torch.Tensor:
        a1 = torch.nn.functional.relu(self.l1(input))
        a2 = torch.nn.functional.relu(self.l2(a1))
        out = self.l3(a2)
        return out


    # stochastic gradient descent
    def sgd(self):
        loader = torch.utils.data.DataLoader(self.dataset, batch_size=32, shuffle=True)
        labels = self.dataset.targets.numpy()  # e.g. array with classes like [0, 1, 5] only

        num_classes = 16  # total classes your model predicts
        unique_classes = np.unique(labels)
        weights_present = compute_class_weight(class_weight='balanced', classes=unique_classes, y=labels)
        full_weights = np.zeros(num_classes, dtype=np.float32)
        for i, cls in enumerate(unique_classes):
            full_weights[cls] = weights_present[i]

        class_weights = torch.tensor(full_weights, dtype=torch.float32)

        criterion = torch.nn.CrossEntropyLoss(weight=class_weights)
        optimizer = torch.optim.Adam(self.parameters(), lr=0.001)

        num_epochs = 10
        for epoch in range(num_epochs):
            self.train()
            total_loss = 0.0
            for batch_data, batch_labels in loader:
                outputs = self(batch_data)
                loss = criterion(outputs, batch_labels)

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                total_loss += loss.item()

            print(f"Epoch {epoch+1}, Loss: {total_loss:.4f}")


    def predict(self, input_normalized) -> int:
        self.eval()
        input_tensor = torch.tensor(input_normalized)
        output_tensor = self.forward(input_tensor)

        selected_i = 0

        for i in range(self.arch[-1]):
            selected_i = i if output_tensor[i].item() > output_tensor[selected_i].item() else selected_i

        return selected_i



class TorchDataset(Dataset):

    def __init__(self, file):
        self.df = pd.read_csv(file)
        self.X = self.df.iloc[:, :-1].values.astype("float32")
        self.y = self.df.iloc[:, -1].values.astype("int64")
        self.targets = torch.tensor(self.y)  

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return torch.tensor(self.X[idx]), torch.tensor(self.y[idx])

