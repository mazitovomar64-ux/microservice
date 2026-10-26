from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, Field, model_validator


class BookingStatus(str, Enum):
    pending = "pending"
    cancelled = "cancelled"
    confirmed = "confirmed"


class BookingCreateSchema(BaseModel):
    hotel_id: int = Field(gt=0)
    room_id: int = Field(gt=0)
    check_in: date
    check_out: date
    guests: int = Field(ge=1, le=20)

    @model_validator(mode="after")
    def validate_dates(self):
        if self.check_in < date.today():
            raise ValueError("Нельзя бронировать прошедшую дату")

        if self.check_out <= self.check_in:
            raise ValueError("Дата выезда должна быть позже даты заезда")

        return self


class BookingUpdateSchema(BaseModel):
    check_in: date | None = None
    check_out: date | None = None
    guests: int | None = Field(default=None, ge=1, le=20)

    @model_validator(mode="after")
    def validate_dates(self):
        if self.check_in is not None and self.check_in < date.today():
            raise ValueError("Нельзя бронировать прошедшую дату")

        if self.check_in is not None and self.check_out is not None:
            if self.check_out <= self.check_in:
                raise ValueError("Дата выезда должна быть позже даты заезда")

        return self


class BookingResponseSchema(BaseModel):
    id: str
    user_id: int
    hotel_id: int
    hotel_name: str
    room_id: int
    room_number: int
    check_in: date
    check_out: date
    nights: int
    guests: int
    price: int
    total_price: int
    status: BookingStatus
    created_date: datetime
    update_date: datetime