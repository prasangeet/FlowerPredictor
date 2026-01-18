from torchvision import transforms

def get_inference_transforms(cfg):
    prep_cfg = cfg["preprocessing"]

    inference_transforms = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(prep_cfg['image_size']),
        transforms.ToTensor(),
        transforms.Normalize(
            mean = prep_cfg['mean'],
            std = prep_cfg['std']
        )
    ])

    return inference_transforms
