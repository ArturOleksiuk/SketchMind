from pathlib import Path

import matplotlib.pyplot as plt 
import numpy as np

from dataset import prepare_splits
from dataset import QuickDrawDataset


data_dir = Path(__file__).resolve().parents[1] / "data"

splits = prepare_splits(data_dir, samples_per_class=10)

print(splits.class_names)
print(sum(len(part.indices) for part in splits.train))

part = splits.train[0] # bicycle
drawings = np.load(part.path, mmap_mode="r")
image = drawings[part.indices[6]].reshape(28, 28)
title = splits.class_names[part.class_id]

plt.imshow(image, cmap="gray", vmin=0, vmax=255)
plt.title(title)
plt.axis("off")
plt.show()

train_dataset = QuickDrawDataset(splits.train)
image, label = train_dataset[10]

print("Shape:", image.shape)
print("Type:", image.dtype)
print("Pixel range:", image.min().item(), image.max().item())
print("Label:", label, splits.class_names[label])

