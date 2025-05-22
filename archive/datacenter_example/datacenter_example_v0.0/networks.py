import torch
import torch.nn as nn
import torch.nn.functional as F
from problog.logic import Constant

class SensorNet(nn.Module):
    def __init__(self, num_classes=2):
        super(SensorNet, self).__init__()
        self.fc1 = nn.Linear(1, 8)
        self.fc2 = nn.Linear(8, num_classes)

    def forward(self, x):
        x = x.view(-1, 1)
        x = F.relu(self.fc1(x))
        return F.softmax(self.fc2(x), dim=1)