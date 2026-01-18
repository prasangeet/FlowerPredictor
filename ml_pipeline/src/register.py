import os
import json
from datetime import datetime

import torch
from torchvision.datasets.sbd import shutil

def register_model(model, metrics, cfg, class_to_idx):
    """
    Saves versioned model with:
    - model weights
    - metrics
    - traning configuration
    - class to index mapping
    """

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_root = cfg["artifacts"]["model_dir"]
    model_dir = os.path.join(model_root, f"flower_model_{timestamp}")

    os.makedirs(model_dir, exist_ok= True)

    # 1. Save model weights
    torch.save(model.state_dict(), os.path.join(model_dir, "model.pth"))

    # 2. Save metrics
    with open(os.path.join(model_dir, "metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2)

    # 3. Save class to index mapping
    with open(os.path.join(model_dir, "class_to_idx.json"), "w") as f:
        json.dump(class_to_idx, f, indent=2)

    # 4. Save training configuration
    config_path = os.path.abspath("ml_pipeline/params.yaml")
    shutil.copy(config_path, os.path.join(model_dir, "params.yaml"))


    return model_dir
