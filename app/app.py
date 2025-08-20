from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.routers import fit_model, predict_value, plot, load_test

app = FastAPI(
    title="Time Series Anomaly Detection API",
    version="0.0.0",
)

Instrumentator().instrument(app).expose(app)

app.include_router(fit_model.router)
app.include_router(predict_value.router)
app.include_router(plot.router)
app.include_router(load_test.router)

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