from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.model_manager import ModelManager
from app.routers import fit_model, predict_value

app = FastAPI(
    title="Time Series Anomaly Detection API",
    version="0.0.0",
)

model_manager = ModelManager()

def get_model_manager():
    return model_manager

app.include_router(fit_model.router)
app.include_router(predict_value.router)

cors_regex = (
    r"^http:\/\/localhost.*$|"
    r"http:\/\/127\.0\.0\.1.*$"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)