from pathlib import Path

import matplotlib.pyplot as plt 
import numpy as np

SAMPLES_PER_CLASS = 5
TRAIN_PERCENT = 60
VALIDATION_PERCENT = 20
SEED_NUMBER = 42

data_dir = Path(__file__).resolve().parents[1] / "data"

class_names = sorted(path.stem for path in data_dir.glob("*.npy"))

if not class_names:
    raise SystemExit(f"No Quick Draw .npy files found in {data_dir}")

train_image_batches = []
test_image_batches = []
validation_image_batches = []

train_label_batches = []
test_label_batches = []
validation_label_batches = []

rng = np.random.default_rng(SEED_NUMBER)

for class_id, class_name in enumerate(class_names):
    drawings  = np.load(data_dir / f"{class_name}.npy", mmap_mode="r")

    indices = rng.choice(len(drawings ), size=SAMPLES_PER_CLASS, replace=False)
    samples = drawings[indices]

    total = len(samples)
    train_count = total * TRAIN_PERCENT // 100
    validation_count = total * VALIDATION_PERCENT // 100
    validation_end = train_count + validation_count

    train_image_batches.append(samples[:train_count])
    validation_image_batches.append(samples[train_count:validation_end])
    test_image_batches.append(samples[validation_end:])

    sample_labels = np.full(len(samples), class_id, dtype="int64")

    train_label_batches.append(sample_labels[:train_count])
    validation_label_batches.append(sample_labels[train_count:validation_end])
    test_label_batches.append(sample_labels[validation_end:])
    
    print(class_id, class_name)

train_images = np.concatenate(train_image_batches, axis=0)
validation_images = np.concatenate(validation_image_batches, axis=0)
test_images = np.concatenate(test_image_batches, axis=0)

train_labels = np.concatenate(train_label_batches, axis=0)
validation_labels = np.concatenate(validation_label_batches, axis=0)
test_labels = np.concatenate(test_label_batches, axis=0)



if len(train_images) == 0:
    raise SystemExit("The local dataset files contain no sketches.")

for name, images, labels in [
    ("train", train_images, train_labels),
    ("validation", validation_images, validation_labels),
    ("test", test_images, test_labels),
]:
    print(name, images.shape, labels.shape)
    print("Кількість за класами:", np.bincount(labels, minlength=len(class_names)))

index = 3 
label = train_labels[index]

plt.imshow(train_images[index].reshape(28, 28), cmap="gray", vmin=0, vmax=255)
plt.title(f"{class_names[label]} (label {label})")
plt.axis("off")
plt.show()