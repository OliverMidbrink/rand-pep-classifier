import torch
import torch.nn as nn

class SimpleAutoregressiveModel(nn.Module):
    def __init__(self):
        super(SimpleAutoregressiveModel, self).__init__()
        self.fc = nn.Linear(100 * 23, 23)

    def forward(self, x):
        x = self.fc(x)
        return x

