import numpy as np

from app.schemas.schema import DataPoint, TimeSeries

class AnomalyDetectionModel:

    def __init__(self, mean: float = 0.0, std: float = 1.0):
        self.mean = mean
        self.std = std

    @classmethod
    def set_params(cls, mean: float, std: float) -> None:
        return cls(mean=mean, std=std)

    def fit(self, data: TimeSeries) -> None:
        values_stream = [d.value for d in data.data]
        self.mean = np.mean(values_stream)
        self.std = np.std(values_stream)

    def predict(self, data_point: DataPoint) -> bool:
        return bool(data_point.value > self.mean + 3 * self.std)
