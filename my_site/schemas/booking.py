from pydantic import BaseModel, Field, model_validator
from enum import Enum
from datetime import date, datetime


class BookingStatus(str, Enum):
    pending = 'pending'
    cancelled = 'cancelled'
    confirmed = 'confirmed'


class BookingCreateSchema(BaseModel):
    hotel_id: str = Field(gt=0)
    room_id: str = Field(gt=0)
    check_in: date
    check_out: date
    quests: int = Field(ge=1, le=20)

    @model_validator(mode='after')
    def validate_dates(self):
        if self.check_out <=self.check_in:
            raise ValueError('Дата выезда должна быть позже даты заезда')


class BookingUpdateSchema(BaseModel):
    check_in: date | None
    check_out: date | None
    quests: int | None = Field(ge=1, le=20)


class BookingResponseSchema(BaseModel):
    id: str
    user_id: int
    hotel_id: int
    hotel_name: str
    room_id: int
    room_number: int
    check_in: date
    check_out: date
    guests: int
    price: int
    total_price: int
    status: BookingStatus
    created_date: datetime
    update_date: datetime