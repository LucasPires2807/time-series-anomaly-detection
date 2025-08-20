from pydantic import BaseModel

class FitResponse(BaseModel):
    series_id: str
    version: str
    points_used: int


class PredictResponse(BaseModel):
    anomaly: bool
    model_version: str


class SystemMetric(BaseModel):
    timestamp: float 
    cpu_percent: float 
    memory_percent: float


class LoadTestResponse(BaseModel):
    duration_seconds: float
    total_requests: int
    requests_per_second: float
    system_metrics: list[SystemMetric]