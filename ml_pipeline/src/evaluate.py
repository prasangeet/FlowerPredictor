import torch

def evaluate(model, dataloader, criterion, device):
    """
    Evaluates the model on the validation dataset.

    Args:
        model: The trained model to evaluate.
        dataloader: DataLoader for the validation dataset.
        criterion: Loss function.
        device: Device to run the evaluation on (CPU or GPU).

    Returns:
        A dictionary containing validation loss and accuracy.
    """
    model.eval()
    running_loss = 0.0
    correct_predictions = 0
    total_samples = 0

    with torch.no_grad():
        for inputs, labels in dataloader:
            inputs, labels = inputs.to(device), labels.to(device)

            outputs = model(inputs)
            loss = criterion(outputs, labels)

            running_loss += loss.item() * inputs.size(0)
            _, preds = torch.max(outputs, 1)
            correct_predictions += torch.sum(preds == labels).item()
            total_samples += inputs.size(0)

    epoch_loss = running_loss / total_samples
    epoch_accuracy = correct_predictions / total_samples

    return {
        "val_loss": epoch_loss,
        "val_accuracy": epoch_accuracy
    }
