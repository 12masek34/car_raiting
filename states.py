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
