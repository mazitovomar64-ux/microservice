import httpx
from fastapi import HTTPException
from my_site.config import settings


async def get_object(url: str):
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(url)

    except httpx.RequestError:
        raise HTTPException(status_code=500, detail='Hotel Service недоступен')

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail='Страница не найдено')

    if response.status_code != 200:
        raise HTTPException(status_code=503, detail='Ошибка')


    try:
        return response.json()

    except ValueError:
        raise HTTPException(status_code=500, detail='Неправильные данные')


async def get_hotel(hotel_id: int):
    url = f'{settings.hotel_service_url}/hotel/{hotel_id}/'

    return await get_object(url=url)



async def get_room(room_id: int):
    url = f'{settings.hotel_service_url}/room/{room_id}/'

    return await get_object(url=url)