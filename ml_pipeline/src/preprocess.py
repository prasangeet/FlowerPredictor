from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import os

def get_dataloader(cfg):
    data_cfg = cfg["data"]
    prep_cfg = cfg["preprocessing"]
    train_cfg = cfg["training"]

    train_transforms = transforms.Compose([
        transforms.RandomResizedCrop(prep_cfg['image_size']),
        transforms.RandomHorizontalFlip(),
        transforms.transforms.ToTensor(),
        transforms.transforms.Normalize(
            mean = prep_cfg['mean'],
            std = prep_cfg['std']
        )
    ])

    val_transforms = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(prep_cfg['image_size']),
        transforms.ToTensor(),
        transforms.Normalize(
            mean = prep_cfg['mean'],
            std = prep_cfg['std']
        )
    ])

    train_dir = os.path.join(data_cfg['root_dir'], data_cfg['train_dir'])
    val_dir = os.path.join(data_cfg['root_dir'], data_cfg['val_dir'])

    train_dataset = datasets.ImageFolder(root= train_dir,  transform= train_transforms)
    val_dataset = datasets.ImageFolder(root= val_dir, transform= val_transforms)

    train_loader = DataLoader(
        train_dataset,
        batch_size= train_cfg['batch_size'],
        shuffle= True,
        num_workers= train_cfg['num_workers'],
        pin_memory= True
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size= train_cfg['batch_size'],
        shuffle= False,
        num_workers= train_cfg['num_workers'],
        pin_memory= True
    )

    return train_loader, val_loader, train_dataset.class_to_idx
