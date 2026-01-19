import torch
from mlflow.pyfunc.model import PythonModel
from mlflow.pyfunc.model import PythonModelContext
from typing import Any


class TorchImageClassifier(PythonModel):
    def __init__(self, model):
        self.model = model

    def predict(
        self,
        context: PythonModelContext,
        model_input,
        params: dict[str, Any] | None = None,
    ):
        # Explicitly reference unused params to satisfy linters
        _ = context
        _ = params

        self.model.eval()
        with torch.no_grad():
            inputs = torch.from_numpy(model_input).float()
            outputs = self.model(inputs)
            return outputs.cpu().numpy()

