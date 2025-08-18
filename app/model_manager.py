from http import HTTPStatus
import re
import threading

from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.config.db.database import get_db
from app.repository.model_repository import ModelRepository
from app.schema import DataPoint, TimeSeries
from app.model import AnomalyDetectionModel


class ModelManager:
    def __init__(self, session: Session):
        self._repository = ModelRepository(session=session)


    def fit(self, series_id: str, time_series: TimeSeries):
        model = AnomalyDetectionModel()
        model.fit(time_series)

        if not time_series.data:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Time series data is empty."
            )
        time_series_db_id = self._repository.get_series_db_id(series_id)
        if not time_series_db_id:
            time_series_db_id = self._repository.create_time_series(series_id).id

        self._repository.add_data_point(
            data_point=time_series,
            time_series_id=time_series_db_id
        )
        version = self._repository.add_model(
            model,
            time_series_id=time_series_db_id,
        )

        return {
            "series_id": series_id,
            "version": version,
            "points_used": len(time_series.data)
        }

    def predict(self, series_id: str, version: str, data_point: DataPoint):
        model = self._repository.get_model(series_id, version)
        if not model:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Model with series_id {series_id} and version {version} not found."
            )

        return {
            "anomaly": model.predict(data_point),
            "model_version": version
        }


def get_model_manager(session=Depends(get_db)) -> ModelManager:
    return ModelManager(session=session)