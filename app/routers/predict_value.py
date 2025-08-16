from http import HTTPStatus
from fastapi import APIRouter, Depends

from app.model_manager import ModelManager, get_model_manager
from app.schema import DataPoint

router = APIRouter(tags=["Prediction"])

@router.post("/predict/{series_id}", status_code=HTTPStatus.OK)
def predict(
    series_id: str,
    data_point: DataPoint,
    version: str,
    manager: ModelManager = Depends(get_model_manager),
):
    return manager.predict(
        series_id=series_id,
        data_point=data_point,
        version=version
    )
