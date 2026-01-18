FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy only inference code (NOT training)
COPY ml_pipeline/inference/ ml_pipeline/inference/

# Install inference-only dependencies
RUN pip install --no-cache-dir -r ml_pipeline/inference/requirements.txt

# Default command: inference CLI
ENTRYPOINT ["python", "-m", "ml_pipeline.inference.predict"]

