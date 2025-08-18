from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config.db.models import ModelVersion, TimeSeries, DataPoint

class PlotTrainingRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_training_serie(self, series_id: str, version: str):
        query = (
            select(DataPoint.timestamp, DataPoint.value)
            .join(TimeSeries, TimeSeries.id == DataPoint.time_series_id)
            .order_by(DataPoint.timestamp)
            .where(TimeSeries.series_id == series_id, TimeSeries.version == version)
        )

        time_series = (await self._session.execute(query)).mappings().all()

        if not time_series:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Time series {series_id} with version {version} not found."
            )
        
        return time_series
    
    async def get_params(self, series_id: str, version: str):
        query = (
            select(ModelVersion.mean, ModelVersion.std)
            .join(TimeSeries, TimeSeries.id == ModelVersion.time_series_id)
            .where(TimeSeries.series_id == series_id, TimeSeries.version == version)
        )

        params = (await self._session.execute(query)).mappings().first()

        if not params:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Model params not found for time series {series_id} with version {version}."
            )
        
        return params