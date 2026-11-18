import torch

from pathlib import Path
from model import SketchCNN
from torch.utils.data import DataLoader
from training.dataset import QuickDrawDataset, prepare_splits

data_dir = Path(__file__).resolve().parents[0] / "data"

splits = prepare_splits(data_dir, samples_per_class=10)
dataset = QuickDrawDataset(splits.train)
loader = DataLoader(dataset, batch_size=8, shuffle=True) # (8, 1, 28, 28)

model = SketchCNN(num_classes=len(splits.class_names))

images, labels = next(iter(loader))
scores = model(images)

loss_function = torch.nn.CrossEntropyLoss()
loss = loss_function(scores, labels)

print("Labels: ", labels)
print("Loss", loss.item())