# Flower Image Classification – MLOps Pipeline (GPU + MLflow + Docker)

This repository contains an **end-to-end MLOps-style image classification pipeline** built using **PyTorch**, **Docker**, and **MLflow**, with **GPU acceleration** support.  
The project trains a CNN (ResNet-based) model on a flower classification dataset and tracks experiments, metrics, and models using MLflow.

---

## 🚀 Features

- 🔥 **GPU-accelerated training** (CUDA + NVIDIA Docker)
- 🧠 **PyTorch model training** (ResNet backbone)
- 📦 **Dockerized pipeline**
- 📊 **MLflow experiment tracking**
- 🧾 **Model + metrics + artifacts logging**
- 🧩 **Clean MLOps separation** (training, evaluation, registration)
- 🧪 Reproducible experiments via configuration files

---

## 🗂️ Project Structure

```
Image Classification/
├── data/
│   └── flower_data/          # Dataset (mounted into container)
│
├── ml_pipeline/
│   ├── params.yaml           # Training & model configuration
│   ├── run_pipeline.py       # Main training + MLflow pipeline
│   ├── outputs/              # Metrics JSON outputs
│   ├── models/               # Saved / registered models
│   └── src/
│       ├── preprocess.py     # Dataloader & transforms
│       ├── train.py          # Model construction
│       ├── evaluate.py       # Validation logic
│       ├── register.py       # Model registry logic
│       └── mlflow_wrapper.py # MLflow PyFunc wrapper
│
├── mlruns/                   # MLflow tracking directory (mounted)
├── Dockerfile
└── README.md
```

---

## ⚙️ Requirements

### Host System

- Linux (Fedora recommended)
- NVIDIA GPU
- NVIDIA Drivers installed (`nvidia-smi` must work)
- Docker
- NVIDIA Container Toolkit

### Python (for MLflow UI)

- Python 3.10+
- `mlflow`

---

## 🐳 Docker Setup (GPU Enabled)

### Build the training image

```bash
docker build -t flower-ml-pipeline .
```

### Run training with GPU

```bash
docker run --rm   --gpus all   --shm-size=8g   -v $(pwd)/data/flower_data:/data/flower_data   -v $(pwd)/ml_pipeline/models:/app/ml_pipeline/models   -v $(pwd)/ml_pipeline/outputs:/app/ml_pipeline/outputs   -v $(pwd)/mlruns:/app/mlruns   flower-ml-pipeline
```

You should see in logs:

```
cuda
Epoch 1/...
```

---

## 📊 Viewing MLflow UI

MLflow UI runs **outside the training container** and reads the same `mlruns/` directory.

### Start MLflow UI (recommended)

```bash
mlflow ui   --backend-store-uri ./mlruns   --host 0.0.0.0   --port 5000
```

Open in browser:

```
http://localhost:5000
```

---

## 🧪 Experiment Tracking

Each run logs:

- Training loss & accuracy (per epoch)
- Validation loss & accuracy
- Model artifacts
- Class-to-index mapping
- Configuration parameters

Experiments are created automatically using:

```python
mlflow.set_experiment("flowers_classification")
```

---

## 🧠 Model Logging Strategy

- Uses **MLflow PyFunc** (framework-agnostic)
- Custom wrapper: `TorchImageClassifier`
- Logs:
  - Model
  - Input signature
  - Input example
  - Metadata artifacts

This makes the model **portable** for:

- FastAPI inference
- Batch prediction
- Future ZenML integration

---

## 🧹 Fixing MLflow UI Issues (if needed)

If MLflow UI shows **“No experiments created”**, clean corrupted folders:

```bash
rm -rf mlruns/1
```

Then restart MLflow UI.

---

## 🛣️ Next Extensions

- 🚀 FastAPI inference service
- 🧠 Top-k predictions + confidence scores
- 📦 MLflow Model Registry (Staging / Production)
- 🔁 ZenML pipeline integration
- ⚡ Mixed precision training (AMP)

---

## 🧑‍💻 Author Notes

This project is designed as a **learning-to-production bridge**:

- Not a toy notebook
- Not over-engineered
- Clean, debuggable, extensible

---

## 📜 License

MIT License
