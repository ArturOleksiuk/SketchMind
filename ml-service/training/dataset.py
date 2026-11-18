from dataclasses import dataclass
from pathlib import Path
from torch.utils.data import Dataset

import numpy as np
import torch

DEFAULT_SEED = 42
DEFAULT_SAMPLES_PER_CLASS = 5_000
TRAIN_PERCENT = 80
VALIDATION_PERCENT = 10

@dataclass
class CategorySplit:
    path: Path
    class_id: int
    indices: np.ndarray

@dataclass
class DatasetSplits:
    train: list[CategorySplit]
    validation: list[CategorySplit]
    test: list[CategorySplit]
    class_names: list[str]

def prepare_splits(
    data_dir: Path,
    *,
    samples_per_class: int | None = DEFAULT_SAMPLES_PER_CLASS,
    seed: int = DEFAULT_SEED,
) -> DatasetSplits:
    
    if not data_dir.is_dir():
        raise FileNotFoundError(f"Dataset directory not found: {data_dir}")
    
    class_names = sorted(path.stem for path in data_dir.glob("*.npy"))

    if not class_names:
        raise FileNotFoundError(f"No .npy files found in {data_dir}")
    
    rng = np.random.default_rng(seed)

    train_data = []
    validation_data = []
    test_data = []
    
    for class_id , class_name in enumerate(class_names):
        path = data_dir / f"{class_name}.npy"
        drawings  = np.load(path, mmap_mode="r")

        if (samples_per_class is None):
            indices = rng.choice(len(drawings), size=len(drawings), replace=False)
        else:
            indices = rng.choice(len(drawings), size=samples_per_class , replace=False)


        total = len(indices)
        train_end = total * TRAIN_PERCENT // 100
        validation_end = train_end + total * VALIDATION_PERCENT // 100

        train_data.append(
            CategorySplit(
                path=path,
                class_id=class_id,
                indices=indices[:train_end]
            )
        )

        validation_data.append(
            CategorySplit(
                path=path,
                class_id=class_id,
                indices=indices[train_end:validation_end]
            )
        )

        test_data.append(
            CategorySplit(
                path=path,
                class_id=class_id,
                indices=indices[validation_end:]
            )
        )

    return DatasetSplits(
        train=train_data,
        validation=validation_data,
        test=test_data,
        class_names=class_names
    )

class QuickDrawDataset(Dataset):
    def __init__(self, parts: list[CategorySplit]):
        self.parts = parts

    def __len__(self) -> int:
        return sum(len(part.indices) for part in self.parts)

    def __getitem__(self, index: int) -> tuple[torch.Tensor, int]:
        remaining = index
        found = None
        
        for part in self.parts:
            part_size = len(part.indices)

            if remaining < part_size:
                row_index = part.indices[remaining]
                found = (part, row_index)
                break

            remaining -= part_size

        if found is None:
            raise IndexError(f"Dataset index out of range: {index}")

        part, row_index = found

        drawings = np.load(part.path, mmap_mode="r")
        image = drawings[row_index]

        image = image.astype(np.float32)
        image = image / 255.0
        image = image.reshape(1, 28, 28)

        return torch.from_numpy(image), part.class_id