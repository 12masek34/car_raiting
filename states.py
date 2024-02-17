from aiogram.fsm.state import (
    State,
    StatesGroup,
)


class CarState(StatesGroup):
    restriction = State()
    keys = State()
    tires = State()
    driver_type = State()
    document_photo = State()
    car_photo_1 = State()
    car_photo_2 = State()
    car_photo_3 = State()
    car_photo_4 = State()
    car_photo_5 = State()
    car_photo_6 = State()
    car_photo_7 = State()
    car_photo_8 = State()
