from http import HTTPStatus
from fastapi import HTTPException
from typing import Sequence

from pydantic import BaseModel, Field, field_validator, model_validator

class DataPoint(BaseModel):
    timestamp: int = Field(..., description="Unix timestamp of the time the data point was collected")
    value: float = Field(..., description="Value of the time series measured at time `timestamp`")

    @field_validator("timestamp")
    def validate_timestamp(cls, v):
        if v < 0:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="timestamp must be a positive Unix timestamp"
            )
        return v


class TimeSeries(BaseModel):
    data: Sequence[DataPoint] = Field(..., description="List of datapoints, ordered by time")

    @model_validator(mode="after")
    def validate_and_sort(cls, values):
        data = values.data if values.data is not None else []

        if len(data) < 10:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Time series must contain at least 10 data points"
            )

        values_set = set()
        timestamps_set = set()

        for dp in data:
            if not isinstance(dp, DataPoint):
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail="All items in data must be DataPoint instances"
                )
            values_set.add(dp.value)
            timestamps_set.add(dp.timestamp)
        
        if len(values_set) == 1:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Cannot send constant values."
            )
        
        if len(timestamps_set) == 1:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Cannot send constant timestamps."
            )

        values.data = sorted(data, key=lambda dp: dp.timestamp)
        return values
