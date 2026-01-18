import os
from typing import Dict, Optional, Tuple
from sympy.polys.polyoptions import Option
import torch
import json
import torch.nn as nn
from torchvision import models
from torchvision.models import ResNet18_Weights

def get_latest_model_dir(models_root : str) -> str:
    """
    Returns the path to the latest model directory based on versioning.
    """

    model_dirs = [
        d for d in os.listdir(models_root)
        if d.startswith("flower_model_")
        and os.path.isdir(os.path.join(models_root,d))
    ]

    if not model_dirs:
        raise RuntimeError("No model directories found.")

    model_dirs.sort()
    latest_model = model_dirs[-1]

    return os.path.join(models_root, latest_model)

def get_model_artifacts(models_root: str) -> Tuple[str, str, str]:
    """
    Returns the paths to model.pth, class_to_idx.json, and model version
    """

    model_dir = get_latest_model_dir(models_root)

    model_path = os.path.join(model_dir, "model.pth")
    class_mapping_path = os.path.join(model_dir, "class_to_idx.json")
    model_version = os.path.basename(model_dir)

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")

    if not os.path.exists(class_mapping_path):
        raise FileNotFoundError(f"Class mapping file not found at {class_mapping_path}")

    return model_path, class_mapping_path, model_version

def load_model_for_inference(models_root: str, device: torch.device):
    """
    Loads the latest model for inference.
    """

    model_path, class_mapping_path, model_version = get_model_artifacts(models_root)

    with open(class_mapping_path, 'r') as f:
        class_to_idx = json.load(f)

    # Build incer mapping
    idx_to_class = {int(v): k for k, v in class_to_idx.items()}
    
    weights = ResNet18_Weights.DEFAULT
    model = models.resnet18(weights = weights)

    for param in model.parameters():
        param.requires_grad =False

    num_classes = len(class_to_idx)
    model.fc = nn.Linear(model.fc.in_features, num_classes)

    #Load Trained weights
    state_dict = torch.load(model_path, map_location=device)
    model.load_state_dict(state_dict)

    model = model.to(device)
    model.eval()

    return model, idx_to_class, model_version

_CACHED_MODEL: Optional[torch.nn.Module] = None
_CACHED_MAPPING: Optional[dict[int, str]] = None
_CACHED_VERSION: Optional[str] = None
_CACHED_CATEGORY_NAMES: Optional[Dict] = None
_CACHED_DEVICE: Optional[torch.device] = None

def load_category_names(mapping_path: str) -> dict:
    """
    Loads class-id -> human-readable name mapping.
    """
    with open(mapping_path, "r") as f:
        return json.load(f)

def get_cached_model(
    models_root: str,
    device: torch.device,
    cat_to_name_path: str
) -> Tuple[nn.Module, Dict[int, str], Dict,  str]:
    """
    Loads the model once and reuses it for subsequent calls.
    """

    global _CACHED_MODEL, _CACHED_MAPPING, _CACHED_VERSION, _CACHED_CATEGORY_NAMES, _CACHED_DEVICE

    if (_CACHED_MODEL is None) or (_CACHED_DEVICE != device):
        _CACHED_MODEL, _CACHED_MAPPING, _CACHED_VERSION = load_model_for_inference(
            models_root=models_root,
            device=device
        )
        _CACHED_DEVICE = device

    category_names = load_category_names(cat_to_name_path)
    _CACHED_CATEGORY_NAMES = category_names
    assert _CACHED_MODEL is not None
    assert _CACHED_MAPPING is not None
    assert _CACHED_VERSION is not None
    assert _CACHED_CATEGORY_NAMES is not None

    return _CACHED_MODEL, _CACHED_MAPPING,_CACHED_CATEGORY_NAMES, _CACHED_VERSION

