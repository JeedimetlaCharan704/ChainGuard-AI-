"""
ChainGuard AI - Deep Neural Network Architecture (PyTorch)
Model: ChainGuardNet
Description: Multi-layer Deep Neural Network with Batch Normalization,
Dropout regularization, and ReLU activations for Ethereum fraud detection.
"""

import torch
import torch.nn as nn

class ChainGuardNet(nn.Module):
    def __init__(self, input_dim=18):
        super(ChainGuardNet, self).__init__()
        
        # Layer 1: Input to 128 neurons
        self.fc1 = nn.Linear(input_dim, 128)
        self.bn1 = nn.BatchNorm1d(128)
        self.relu1 = nn.ReLU()
        self.dropout1 = nn.Dropout(0.3)
        
        # Layer 2: 128 to 64 neurons
        self.fc2 = nn.Linear(128, 64)
        self.bn2 = nn.BatchNorm1d(64)
        self.relu2 = nn.ReLU()
        self.dropout2 = nn.Dropout(0.2)
        
        # Layer 3: 64 to 32 neurons
        self.fc3 = nn.Linear(64, 32)
        self.bn3 = nn.BatchNorm1d(32)
        self.relu3 = nn.ReLU()
        self.dropout3 = nn.Dropout(0.1)
        
        # Layer 4: Output Layer (1 neuron for binary classification)
        self.fc_out = nn.Linear(32, 1)
        self.sigmoid = nn.Sigmoid()
        
    def forward(self, x):
        # Forward pass through deep layers
        x = self.dropout1(self.relu1(self.bn1(self.fc1(x))))
        x = self.dropout2(self.relu2(self.bn2(self.fc2(x))))
        x = self.dropout3(self.relu3(self.bn3(self.fc3(x))))
        logits = self.fc_out(x)
        probabilities = self.sigmoid(logits)
        return probabilities, logits

def get_model(input_dim=18):
    return ChainGuardNet(input_dim=input_dim)
