from fastapi import FastAPI, HTTPException
import uvicorn
from pymongo.errors import PyMongoError
from my_site.database.mongodb import get_database, close_mongo, connect_mongodb
from contextlib import asynccontextmanager
from my_site.api import bookings


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await connect_mongodb()
        print('Mongodb: Подключение успешно')
        yield
    finally:
        await close_mongo()
        print('Mongodb: соединение закрыто')

booking_app = FastAPI(title='Booking Service', lifespan=lifespan)
booking_app.include_router(bookings.booking_router)

#
# @booking_app.get('/')
# async def test_info():
#     return {"message": 'Все работает'}


# @booking_app.get('/check/database')
# async def check_database():
#     try:
#         database = get_database()
#         await database.command('ping')
#
#         return {'status': 'ok', 'database': database.name, 'connection': 'active'}
#
#     except PyMongoError:
#         raise HTTPException(status_code=500, detail='MongoDB недоступен')


if __name__ == '__main__':
    uvicorn.run(booking_app, host='127.0.0.1', port=8002)



