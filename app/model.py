import numpy as np

from app.schema import DataPoint, TimeSeries

class AnomalyDetectionModel:
    def fit(self, data: TimeSeries) -> None:
        values_stream = [d.value for d in data.data]
        self.mean = np.mean(values_stream)
        self.std = np.std(values_stream)

    def predict(self, data_point: DataPoint) -> bool:
        return bool(data_point.value > self.mean + 3 * self.std)
