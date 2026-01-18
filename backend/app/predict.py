from fastapi import APIRouter, File, HTTPException, UploadFile
from pathlib import Path
import uuid
import subprocess
import json

router = APIRouter()

TMP_DIR = Path("/tmp/inference_uploads")
TMP_DIR.mkdir(parents=True, exist_ok=True)

@router.post('/predict')
async def predict(image: UploadFile = File(...)):
    """
    Mock inference enpoint
    """
    if image.filename is None:
        raise HTTPException(status_code=400, detail="Uploaded file has no filename")

    suffix = Path(image.filename).suffix or '.jpg'
    tmp_path = TMP_DIR / f"{uuid.uuid4()}{suffix}"

    content = await image.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    with open(tmp_path, "wb") as f:
        f.write(content)

    cmd = [
        "docker", "exec",
        "flower-inference",
        "python", "-m", "ml_pipeline.inference.predict",
        "--image", f"/data/input/{tmp_path.name}",
        "--models-root", "/app/ml_pipeline/models",
        "--cat-to-name", "/data/flower_data/cat_to_name.json",
        "--top-k", "5",
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output= True,
            text= True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else e.stdout.strip()
        raise HTTPException(
            status_code=500,
            detail=f"Inference failed: {error_msg}",
        )

    try:
        prediction = json.loads(result.stdout)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail= "Inference returned invalid JSON",
        )

    return prediction
