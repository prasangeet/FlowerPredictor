FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

WORKDIR /app

# Copy only what is needed for training
COPY ml_pipeline/ ml_pipeline/

# Install dependencies
RUN pip install --no-cache-dir -r ml_pipeline/requirements.txt

# Default command
CMD ["python", "ml_pipeline/run_pipeline.py"]

