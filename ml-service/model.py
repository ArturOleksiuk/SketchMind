import torch

from torch import nn

class SketchCNN(nn.Module):
    def __init__(self, num_classes: int):
        super().__init__()

        self.conv1 = nn.Conv2d(
            in_channels=1,
            out_channels=8,
            kernel_size=3,
            padding=1
        ) 

        self.relu = nn.ReLU()

        self.pool = nn.MaxPool2d(kernel_size=2, stride=2) 

        self.conv2 = nn.Conv2d(
            in_channels=8,
            out_channels=16,
            kernel_size=3,
            padding=1
        ) 

        self.flatten = nn.Flatten(start_dim=1)

        self.classifier = nn.Linear(
            in_features=16 * 7 * 7,
            out_features=num_classes
        )

    def forward(self, images: torch.Tensor) -> torch.Tensor:
        features = self.conv1(images) # (1, 8, 28, 28)
        features = self.relu(features)
        features = self.pool(features) # (1, 8, 14, 14)
        features = self.conv2(features) # (1, 16, 14, 14)
        features = self.relu(features)
        features = self.pool(features) # (1, 16, 7, 7)
        
        features = self.flatten(features) # (N, 16, 7, 7) → (N, 784)

        return self.classifier(features)
        
