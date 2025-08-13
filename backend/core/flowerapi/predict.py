import torch
from torchvision import models, transforms
from torch import nn
from PIL import Image
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load class mapping
with open(os.path.join(BASE_DIR, 'class_mapping.json'), 'r') as f:
    cat_to_name = json.load(f)

# Load index-to-class mapping
with open(os.path.join(BASE_DIR, "idx_to_class.json"), "r") as f:
    idx_to_class = json.load(f)

# Device setup
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ----- 1. Recreate model architecture -----
model = models.resnet18(pretrained=False)  # Or the model you used
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, len(cat_to_name))

# ----- 2. Load weights -----
model_path = os.path.join(BASE_DIR, 'best_flower_model.pth')
state_dict = torch.load(model_path, map_location=device)
model.load_state_dict(state_dict)

# ----- 3. Prepare for inference -----
model.to(device)
model.eval()

# Image preprocessing
inference_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

def predict_image(image_file):
    image = Image.open(image_file).convert("RGB")
    img_tensor = inference_transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(img_tensor)
        probs = torch.softmax(outputs, dim=1)
        confidence, pred_idx = torch.max(probs, 1)
        pred_idx = pred_idx.item()
        confidence = confidence.item()

    # ✅ Correct mapping: model index -> dataset class -> flower name
    class_label = idx_to_class[str(pred_idx)]
    flower_name = cat_to_name.get(class_label, "Unknown")

    return {
        "class": flower_name,
        "confidence": confidence
    }
