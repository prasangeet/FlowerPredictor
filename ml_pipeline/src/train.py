import torch
import torchvision.models as models 



def build_model(cfg, device):
    model_cfg = cfg["model"]

    if model_cfg["name"] == 'resnet18':
        if model_cfg['pretrained']:
            weights = models.ResNet18_Weights.DEFAULT
        else:
            weights = None
        model = models.resnet18(weights=weights)
    else:
        raise ValueError(f"Model {model_cfg['model']} not supported.")

    for param in model.parameters():
        param.requires_grad = False

    num_features = model.fc.in_features
    model.fc = torch.nn.Linear(num_features, model_cfg["num_classes"])

    return model.to(device)
