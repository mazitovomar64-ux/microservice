from fastapi import APIRouter, Depends
from my_site.schemas.booking import BookingResponseSchema
from my_site.database.mongodb import get_booking_collections
from my_site.database.mapper import booking_document_to_response
from .dependencies import get_current_user
from typing import Annotated, List


booking_router = APIRouter(prefix='/bookings', tags=['Bookings'])


@booking_router.get('/', response_model=List[BookingResponseSchema])
async def booking_list(current_user: Annotated[dict, Depends(get_current_user)]):
    collection = get_booking_collections()
    cursor = collection.find({'user_id': current_user['id']}).sort('created_date', -1)

    bookings = []

    async for i in cursor:
        bookings.append(booking_document_to_response(i))

    return bookings