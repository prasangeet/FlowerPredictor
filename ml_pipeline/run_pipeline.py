from datetime import datetime
import json
import os
from tqdm import tqdm
import yaml
import random
import numpy as np
import torch

from src import evaluate, register
from src.preprocess import get_dataloader
from src.train import build_model
from src.evaluate import evaluate
from src.register import register_model

def load_config():
    with open("ml_pipeline/params.yaml", "r") as f:
        return yaml.safe_load(f);

def set_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

def main():
    cfg = load_config()
    set_seed(cfg["training"]["seed"])

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # 1. Data
    train_loader, val_loader, class_to_idx = get_dataloader(cfg)

    # 2. Model
    model = build_model(cfg, device)

    # 3. Training setup
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(
        model.fc.parameters(),
        lr= cfg['training']['learning_rate']
    )

    train_losses = []
    train_accuracies = []


    # 4. Training loop (omitted for brevity)
    model.train()
    for epoch in range(cfg["training"]["epochs"]):
        running_loss = 0.0
        running_corrects = 0
        total_samples = 0

        epoch_bar = tqdm(
            train_loader,
            desc=f"Epoch {epoch + 1}/{cfg['training']['epochs']}",
            leave=False
        )

        model.train()
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

        train_losses.append(epoch_loss)
        train_accuracies.append(epoch_acc)

    # 5. Evaluation (omitted for brevity)
    metrics = evaluate(model, val_loader, criterion, device)
    
    os.makedirs(cfg["artifacts"]["output_dir"], exist_ok=True)

    run_metrics = {
        "train_loss": train_losses[-1],
        "train_accuracy": train_accuracies[-1],
        "val_loss": metrics["val_loss"],
        "val_accuracy": metrics["val_accuracy"]
    }

    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    metrics_path = os.path.join(
        cfg["artifacts"]["output_dir"], f"metrics_{run_id}.json"
    )

    with open(metrics_path, "w") as f:
        json.dump(run_metrics, f)

    # 6. Register model (omitted for brevity)
    model_dir = register_model(model, metrics, cfg, class_to_idx)

    print("Pipeline completed")
    print("Model saved to:", model_dir)
    print("Metrics:", metrics)

if __name__ == "__main__":
    main()
