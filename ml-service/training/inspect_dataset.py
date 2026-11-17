from pathlib import Path

import matplotlib.pyplot as plt 
import numpy as np

data_dir = Path(__file__).resolve().parents[1] / "data"
samples_per_class = 5

class_names = ["cat", "car"]

cats = np.load(data_dir / "cat.npy", mmap_mode="r")[:samples_per_class]
cars = np.load(data_dir / "car.npy", mmap_mode="r")[:samples_per_class]

images = np.concatenate([cats, cars])
labels = np.concatenate([
    np.zeros(len(cats), dtype=np.int64),
    np.ones(len(cars), dtype=np.int64),
])

print("Images shape:", images.shape)
print("Labels shape:", labels.shape)
print("Labels:", labels)

index = 6
image = images[index].reshape(28, 28)
label = labels[index]

plt.imshow(image, cmap="gray", vmin=0, vmax=255)
plt.title(f"{class_names[label]} (label {label})")
plt.axis("off")
plt.show()