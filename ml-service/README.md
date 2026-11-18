# SketchMind ML Service

This folder contains the dataset exploration code for SketchMind.

## Dataset

The [Google Quick, Draw! dataset](https://github.com/googlecreativelab/quickdraw-dataset#numpy-bitmaps-npy) provides 28 × 28 grayscale sketches as NumPy `.npy` files. Each file contains sketches from one category.

Place your downloaded Quick, Draw! .npy files in ml-service/data/. The inspection script discovers the category files in that folder, assigns class IDs in alphabetical order by filename, and samples 10 sketches per category. It splits each category into 80% training, 10% validation, and 10% test data. Dataset files are ignored by Git.

With five local category files, the script prints the class names and a training count of 40 sketches. It then displays a sample sketch. After you close the preview window, it prints the shape, data type, pixel range, and class label of one sample loaded by QuickDrawDataset. Each sample is returned as a torch.float32 tensor of shape (1, 28, 28) with pixel values scaled to [0, 1].

## Run locally

From the repository root, run these commands in PowerShell:

```powershell
cd ml-service
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe .\training\inspect_dataset.py
```

If you already have a virtual environment with the dependencies installed, run only the final command from `ml-service/`.

The script prints the class labels and array shapes, then displays one sketch with its class name. With five sketches from each of `bicycle.npy`, `car.npy`, `cat.npy`, `house.npy`, and `tree.npy`, the expected shapes are `(25, 784)` for images and `(25,)` for labels.

## Planned architecture

The training code will use Quick, Draw! to train a PyTorch CNN and save its weights and class order. A separate FastAPI app will load the trained model and classify PNG sketches sent by the ASP.NET Core API.