from datetime import datetime
import json
import os
import random
import yaml
import numpy as np
import torch
from tqdm import tqdm

from src.preprocess import get_dataloader
from src.train import build_model
from src.evaluate import evaluate
from src.register import register_model

import mlflow
from mlflow.models import infer_signature

from src.mlflow_wrapper import TorchImageClassifier


# ------------------------
# Utilities
# ------------------------
def load_config():
    with open("ml_pipeline/params.yaml", "r") as f:
        return yaml.safe_load(f)


def set_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


# ------------------------
# Main pipeline
# ------------------------
def main():
    cfg = load_config()
    set_seed(cfg["training"]["seed"])

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(device)

    # ---- MLflow setup ----
    mlflow.set_experiment("flowers_classification")
    mlflow.end_run()  # safety

    with mlflow.start_run(run_name=cfg["model"]["name"]):
        # ---- Log config ----
        mlflow.log_params({
            "model_name": cfg["model"]["name"],
            "pretrained": cfg["model"]["pretrained"],
            "num_classes": cfg["model"]["num_classes"],
            "learning_rate": cfg["training"]["learning_rate"],
            "batch_size": cfg["training"]["batch_size"],
            "epochs": cfg["training"]["epochs"],
            "optimizer": "Adam",
            "device": device.type,
        })

        # ---- Data ----
        train_loader, val_loader, class_to_idx = get_dataloader(cfg)

        # ---- Model ----
        model = build_model(cfg, device)

        criterion = torch.nn.CrossEntropyLoss()

        optimizer = torch.optim.Adam(
            filter(lambda p: p.requires_grad, model.parameters()),
            lr=cfg["training"]["learning_rate"],
        )

        # ---- Training ----
        model.train()
        for epoch in range(cfg["training"]["epochs"]):
            running_loss = 0.0
            running_corrects = 0
            total_samples = 0

            epoch_bar = tqdm(
                train_loader,
                desc=f"Epoch {epoch + 1}/{cfg['training']['epochs']}",
                leave=False,
            )

            for inputs, labels in epoch_bar:
                inputs = inputs.to(device)
                labels = labels.to(device)

                optimizer.zero_grad()
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()

                _, preds = torch.max(outputs, 1)

                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels).item()
                total_samples += inputs.size(0)

                epoch_bar.set_postfix(loss=loss.item())

            epoch_loss = running_loss / total_samples
            epoch_acc = running_corrects / total_samples

            mlflow.log_metric("train_loss", epoch_loss, step=epoch)
            mlflow.log_metric("train_accuracy", epoch_acc, step=epoch)

        # ---- Evaluation ----
        model.eval()
        metrics = evaluate(model, val_loader, criterion, device)

        mlflow.log_metrics({
            "val_loss": metrics["val_loss"],
            "val_accuracy": metrics["val_accuracy"],
        })

        # ---- Save metrics locally ----
        os.makedirs(cfg["artifacts"]["output_dir"], exist_ok=True)
        run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        metrics_path = os.path.join(
            cfg["artifacts"]["output_dir"], f"metrics_{run_id}.json"
        )

        with open(metrics_path, "w") as f:
            json.dump(metrics, f, indent=4)

        mlflow.log_artifact(metrics_path, artifact_path="metrics")

        # ---- MLflow model logging (CORE API) ----
        example_batch, _ = next(iter(val_loader))
        example_input = example_batch[:1].to(device)

        with torch.no_grad():
            example_output = model(example_input)

        signature = infer_signature(
            example_input.cpu().numpy(),
            example_output.cpu().numpy()
        )

        wrapped_model = TorchImageClassifier(model)

        mlflow.pyfunc.log_model(
            artifact_path='model',
            python_model=wrapped_model,
            signature=signature,
            input_example=example_input.cpu().numpy(),
        )
        # ---- Extra artifacts ----
        mlflow.log_dict(class_to_idx, "class_to_idx.json")

        # ---- Register model (your logic) ----
        model_dir = register_model(model, metrics, cfg, class_to_idx)

        print("✅ Pipeline completed")
        print("📦 Model saved to:", model_dir)
        print("📊 Metrics:", metrics)


if __name__ == "__main__":
    main()

