from http import HTTPStatus
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import StreamingResponse

from app.service.plot_training_service import get_plot_service

router = APIRouter(tags=["Plot"])

@router.post("/plot", status_code=HTTPStatus.OK)
async def plot(
    series_id: str,
    version: str,
    service: AsyncSession = Depends(get_plot_service)
):
    plot_buffer = await service.plot(
        series_id=series_id,
        version=version
    )
    return StreamingResponse(plot_buffer, media_type="image/png")
