from typing import List, Optional

from fastapi import HTTPException
from pydantic import BaseModel, field_validator


class Coordinates(BaseModel):
    latitude: float
    longitude: float


class ExtraField(BaseModel):
    name: str
    description: str
    is_required: bool


# class ExtraFieldPayload(BaseModel):
#     name: str
#     value: str


class DeliveryType(BaseModel):
    name: str
    amount: float = 0.0
    is_address_required: bool = False
    address_hint: Optional[str] = ''
    extra_fields: List[ExtraField] = []
    is_timepicker_required: bool = False
    details: str = ''
    country: Optional[str] = ''
    country_code: Optional[str] = ''  # ISO format, ex.: RU, KZ, BY...
    city: Optional[str] = None
    delivery_location: Optional[Coordinates] = None
    delivery_radius: Optional[int] = None
    delivery_min_hour: Optional[int] = None
    delivery_max_hour: Optional[int] = None
    delivery_minutes_interval: Optional[int] = None
    delivery_min_day: Optional[int] = None
    delivery_max_day: Optional[int] = None

    @field_validator('name')
    def name_validation(cls, name):
        name = name.strip()
        if len(name) <= 2:
            raise HTTPException(status_code=400, detail=f'Invalid delivery name: {name}')
        return name


class DeliveryTypeResponse(DeliveryType):
    id: str
