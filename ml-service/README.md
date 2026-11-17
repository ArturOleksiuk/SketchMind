# SketchMind ML Service

This folder contains the dataset exploration code for SketchMind.

## Dataset

The [Google Quick, Draw! dataset](https://github.com/googlecreativelab/quickdraw-dataset#numpy-bitmaps-npy) provides 28 × 28 grayscale sketches as NumPy `.npy` files. Each file contains sketches from one category.

Place your downloaded category files in `ml-service/data/`. The inspection script discovers the `.npy` files present in that folder, takes up to five sketches per file, and assigns numeric labels in alphabetical order by filename. Dataset files are ignored by Git.

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