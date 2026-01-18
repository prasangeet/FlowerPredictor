from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from .predict import router as predict_router
from .health import router as health_router

load_dotenv()

app = FastAPI()

# Read frontend URLs safely
frontend_urls_env = os.getenv("FRONTEND_URLS") or os.getenv("FRONTEND_URL")

allow_origins = (
    [url.strip() for url in frontend_urls_env.split(",")]
    if frontend_urls_env
    else []
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(predict_router)

