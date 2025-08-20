from http import HTTPStatus
from fastapi import APIRouter

from app.schemas.response_schema import LoadTestResponse
from app.schemas.schema import LoadTestRequest
from app.service.load_test import LoadTest

router = APIRouter(tags=["Load Test"])

@router.post("/load-test", status_code=HTTPStatus.OK, response_model=LoadTestResponse)
async def load_test(request: LoadTestRequest):
    return await LoadTest(**request.model_dump()).load_test()