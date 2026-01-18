from typing import Dict, List
from sympy import arg
from torchvision import models, transforms
from PIL import Image
import torch

from .model_loader import get_cached_model

def get_inference_transform():
    """
    Returns deterministic transforms for inference
    Matches validation preprocessing used during training
    """
    return transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            mean = [0.485, 0.456, 0.406],
            std = [0.229, 0.224, 0.225],
        )
    ])

def load_image(image_path: str, device: torch.device):
    """
    Loads an image from disk and applies inference transforms.
    Returns a tensor of shape [1, C, H, W].
    """
    image = Image.open(image_path).convert("RGB")
    transform = get_inference_transform()
    tensor = transform(image)
    if not isinstance(tensor, torch.Tensor):
        raise TypeError("Transform did not convert the image to a tensor")
    tensor = tensor.unsqueeze(0)
    return tensor.to(device)

def predict(
    image_path: str,
    models_root: str,
    cat_to_name_path: str,
    top_k: int = 5
) -> Dict:
    """
    Runs inference on a single image and returns structured predictions.
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load model and mappings
    model, idx_to_class, cat_to_name, model_version = get_cached_model(
        models_root=models_root,
        device=device,
        cat_to_name_path=cat_to_name_path
    )

    # Load and preprocess image
    image_tensor = load_image(image_path, device)

    with torch.no_grad():
        outputs = model(image_tensor)
        probs = torch.softmax(outputs, dim=1)

        top_probs, top_idxs = probs.topk(top_k)

    top_probs = top_probs.cpu().squeeze(0).cpu().tolist()
    top_idxs = top_idxs.cpu().squeeze(0).cpu().tolist()

    top_predictions: List[Dict] = []
    for prob, idx in zip(top_probs, top_idxs):
        class_id = idx_to_class[idx]
        class_label = cat_to_name.get(class_id, class_id)
        top_predictions.append({
            "class": class_label,
            "confidence": float(prob),
        })

    if not top_predictions:
        raise ValueError("No valid predictions available; ensure correct model or input.")

    return {
        "predicted_class": top_predictions[0]["class"],
        "confidence": top_predictions[0]["confidence"],
        "top_k": top_predictions,
        "model_version": model_version,
    }

import argparse
import json
import sys

def main():
    parser = argparse.ArgumentParser(description="Flower classifier inference")
    parser.add_argument(
        "--image",
        type=str,
        required=True,
        help="Path to input image (jpg/png)"
    )
    parser.add_argument(
        "--models-root",
        type=str,
        default="ml_pipeline/models",
        help="Path to the model registry root"
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        help="Number of top predictions to return",
    )
    parser.add_argument(
        "--cat-to-name",
        type=str,
        required=True,
        help="Path to cat-to-name.json mapping file"
    )

    args = parser.parse_args()

    try:
        result = predict(
            image_path=args.image,
            models_root=args.models_root,
            top_k=args.top_k,
            cat_to_name_path=args.cat_to_name,
        )
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Inference failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

