from http import HTTPStatus
from fastapi import APIRouter, Depends

from app.schemas.response_schema import FitResponse
from app.service.model_manager import ModelManager, get_model_manager
from app.schemas.schema import TimeSeries

router = APIRouter(tags=["Training"])

@router.post("/fit/{series_id}", status_code=HTTPStatus.CREATED, response_model=FitResponse)
async def fit_series(
    series_id: str,
    time_series: TimeSeries,
    manager: ModelManager = Depends(get_model_manager)
):
    return await manager.fit(series_id=series_id, time_series=time_series)
