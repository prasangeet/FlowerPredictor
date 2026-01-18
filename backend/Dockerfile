FROM python:3.11-slim

# Prevent Python buffering
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system deps (needed for curl, docker CLI)
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    docker-cli \
 && rm -rf /var/lib/apt/lists/*

# Copy backend code
COPY backend/app backend/app
COPY backend/requirements.txt backend/requirements.txt

# Install Python deps
RUN pip install --no-cache-dir -r backend/requirements.txt

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]

