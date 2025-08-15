from http import HTTPStatus
import re
import threading

from fastapi import HTTPException

from app.schema import DataPoint, TimeSeries
from app.model import AnomalyDetectionModel


def _increment(match: re.Match):
    number = int(match.group(1))
    return f"v{number + 1}"

class ModelManager:
    def __init__(self):
        self.models_by_series_id: dict = dict()
        self._lock = threading.Lock()


    def fit(self, series_id: str, time_series: TimeSeries):
        model = AnomalyDetectionModel()
        model.fit(time_series)

        with self._lock:
            models_by_series_id = self.models_by_series_id.get(series_id, {})
            version = "v1"

            if models_by_series_id:
                previous_version = max(
                    models_by_series_id.keys(),
                )
                
                version = re.sub(r"v(\d+)", _increment, previous_version)
            else:
                self.models_by_series_id.update({series_id: {}})


            self.models_by_series_id[series_id].update({
                version: model
            })

            return {
                "series_id": series_id,
                "version": version,
                "points_used": len(time_series.data)
            }

    def predict(self, series_id: str, version: str, data_point: DataPoint):
        with self._lock:
            models_by_series_id: dict = self.models_by_series_id.get(series_id, {})
            if not models_by_series_id:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=f"Series id {series_id}  not avaliable."
                )

            model_version: AnomalyDetectionModel = models_by_series_id.get(version)
            if not model_version:
                avaliable_versions = " ".join(models_by_series_id.keys())
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=(
                        f"The version {version} is not avaliable. Try "
                        f"any of the avaliable options:\n\n {avaliable_versions}."
                    )
                )
            
            return {
                "anomaly": model_version.predict(data_point),
                "model_version": version
            }