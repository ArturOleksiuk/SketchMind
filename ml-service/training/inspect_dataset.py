from pathlib import Path

import matplotlib.pyplot as plt 
import numpy as np

data_dir = Path(__file__).resolve().parents[1] / "data"

class_names = sorted(path.stem for path in data_dir.glob("*.npy"))

if not class_names:
    raise SystemExit(f"No Quick Draw .npy files found in {data_dir}")

image_batches = []
label_batches = []

for class_id, class_name in enumerate(class_names):
    samples = np.load(data_dir / f"{class_name}.npy", mmap_mode="r")[:5]
    sample_labels = np.full(len(samples), class_id, dtype="int64")

    image_batches.append(samples)
    label_batches.append(sample_labels)
    
    print(class_id, class_name)

images = np.concatenate(image_batches, axis=0)
labels = np.concatenate(label_batches, axis=0)

if len(images) == 0:
    raise SystemExit("The local dataset files contain no sketches.")

print("Images shape:", images.shape)
print("Labels shape:", labels.shape)
print("Labels:", labels)

index = 8 
label = labels[index]

plt.imshow(images[index].reshape(28, 28), cmap="gray", vmin=0, vmax=255)
plt.title(f"{class_names[label]} (label {label})")
plt.axis("off")
plt.show()