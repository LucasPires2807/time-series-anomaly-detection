from http import HTTPStatus
import uuid
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, func
from app.config.db.models import DataPoint, ModelVersion, TimeSeries
from sqlalchemy.orm import Session

from app.model import AnomalyDetectionModel
from app.schema import TimeSeries as TimeSeriesSchema

class ModelRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_data_point(self, data_point: TimeSeriesSchema, time_series_id: uuid.UUID) -> None:
        try:
            self.session.bulk_insert_mappings(
                DataPoint,
                [
                    {
                        "time_series_id": time_series_id,
                        "timestamp": dp.timestamp,
                        "value": dp.value
                    }
                    for dp in data_point.data
                ]
            )
            self.session.commit()
        except IntegrityError as e:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=f"Tried to insert a timestamp already that already exists in database."
            )

    def create_time_series(self, series_id: str) -> TimeSeries:
        time_series = TimeSeries(
            series_id=series_id,
            version="v1",
            description=None
        )
        self.session.add(time_series)
        self.session.commit()
        self.session.refresh(time_series)
        return time_series

    def get_series_db_id(self, series_id: str) -> uuid.UUID | None:
        query = select(
            TimeSeries.id
        ).where(
            TimeSeries.series_id == series_id
        )
        result = self.session.execute(query).scalar()
        return result

    def get_next_version(self, time_series_id: uuid.UUID) -> str:
        query = (
            select(func.max(ModelVersion.version))
            .where(ModelVersion.time_series_id == time_series_id)
            .with_for_update()
        )
        result = self.session.execute(query).scalar()
        if result is None:
            return "v1"
        number = int(result[1:])
        return f"v{number + 1}"

    def add_model(self, model: AnomalyDetectionModel, time_series_id: uuid.UUID) -> str:
        version = ""
        if not time_series_id:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Time series with ID {series_id} not found."
            )
        with self.session.begin():
            version = version or self.get_next_version(time_series_id)
            model = ModelVersion(
                time_series_id=time_series_id,
                version=version,
                mean=model.mean,
                std=model.std
            )
            self.session.add(model)
        return version

    def get_model(self, series_id: str, version: str) -> AnomalyDetectionModel:
        query = (
            select(ModelVersion)
            .join(TimeSeries, ModelVersion.time_series_id == TimeSeries.id)
            .where(TimeSeries.series_id == series_id, ModelVersion.version == version)
        )
        result = self.session.execute(query).scalars().first()
        if not result:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Model with series_id {series_id} and version {version} not found."
            )
        return AnomalyDetectionModel.set_params(
            mean=result.mean,
            std=result.std
        )