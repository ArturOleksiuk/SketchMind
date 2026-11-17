# SketchMind ML Service

This folder contains the dataset exploration code for SketchMind. The inspection script loads Google Quick, Draw! sketches, assigns class labels, and displays a sample.

## Dataset

Google Quick, Draw! provides 28 × 28 grayscale sketches as NumPy `.npy` files. Each file contains drawings from a single category. See the [Quick, Draw! dataset documentation](https://github.com/googlecreativelab/quickdraw-dataset#numpy-bitmaps-npy).

Place `cat.npy` and `car.npy` in `ml-service/data/` to run the inspection script. Dataset files are kept locally and ignored by Git.

## Run locally

From the repository root, run these commands in PowerShell:

```powershell
cd ml-service
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe .\training\inspect_dataset.py
```

The script prints the shapes of the image and label arrays, then displays one sketch with its class label. With five samples per class, the expected shapes are `(10, 784)` for images and `(10,)` for labels.

## Planned architecture

The training code will use Quick, Draw! to train a PyTorch CNN and save its weights and class order. A separate FastAPI app will load those weights and classify PNG sketches sent by the ASP.NET Core API.