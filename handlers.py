from aiogram import (
    Bot,
    Router,
    types,
)
from aiogram.filters import (
    Command,
)
from aiogram.fsm.context import (
    FSMContext,
)

from database.connection import (
    Db,
)
from states import CarState

router = Router()
# bot.send_document(config.GROUP_ID, document_id)


@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext, db: Db):
    user_id = message.from_user.id
    await db.add_car(user_id)
    button_yes = types.KeyboardButton(text="да")
    button_no = types.KeyboardButton(text="нет")
    keyboard = types.ReplyKeyboardMarkup(keyboard=[[button_yes, button_no]], resize_keyboard=True)
    await message.answer("Есть ли текущий залог или ограничение на авто?", reply_markup=keyboard)
    await state.set_state(CarState.restriction)


@router.message(CarState.document_photo)
async def document(message: types.Message, state: FSMContext, db: Db):
    document_id = getattr(message.document, "file_id", None)
    photo_id = getattr(message.photo, "file_id", None)
    user_id = message.from_user.id
    await db.add_document(user_id, document_id, photo_id)
    await message.answer("aaaaaaaaaaaaaaaAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    await state.set_state(CarState.car_photo_1)


@router.message(CarState.driver_type)
async def drive_type(message: types.Message, state: FSMContext, db: Db):
    user_id = message.from_user.id
    drive_type = message.text
    await db.add_drive_type(user_id, drive_type)
    await message.answer(
        "Сделать Фото СТС или ПТС с читаемыми данными. Без бликов и размытости.",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await state.set_state(CarState.document_photo)


@router.message(CarState.tires)
async def tires(message: types.Message, state: FSMContext, db: Db):
    user_id = message.from_user.id
    tire = message.text
    await db.add_tire(user_id, tire)
    button_drive_type_front = types.KeyboardButton(text="передний")
    button_drive_type_rear = types.KeyboardButton(text="задний")
    button_drive_type_full = types.KeyboardButton(text="полный")
    keyboard = types.ReplyKeyboardMarkup(keyboard=[[
        button_drive_type_front,
        button_drive_type_rear,
        button_drive_type_full,
    ]], resize_keyboard=True)
    await message.answer("Какой привод на авто?", reply_markup=keyboard)
    await state.set_state(CarState.driver_type)


@router.message(CarState.keys)
async def keys(message: types.Message, state: FSMContext, db: Db):
    user_id = message.from_user.id
    number_of_keys = int(message.text) if message.text.isdigit() else None
    await db.add_number_of_keys(user_id, number_of_keys)
    button_tire_disable = types.KeyboardButton(text="отсутствует")
    button_tire_winter = types.KeyboardButton(text="зимняя")
    button_tire_summer = types.KeyboardButton(text="летняя")
    button_tire_mud = types.KeyboardButton(text="грязевая")
    keyboard = types.ReplyKeyboardMarkup(keyboard=[[
        button_tire_disable,
        button_tire_winter,
        button_tire_summer,
        button_tire_mud,
    ]], resize_keyboard=True)
    await message.answer("Есть ли доп. комплект резины?", reply_markup=keyboard)
    await state.set_state(CarState.tires)


@router.message(CarState.restriction)
async def restriction(message: types.Message, state: FSMContext, db: Db):
    user_id = message.from_user.id
    restricion = True if message.text.lower() == "да" else False
    await db.add_restriction(user_id, restricion)
    button_1 = types.KeyboardButton(text="1")
    button_2 = types.KeyboardButton(text="2")
    button_3 = types.KeyboardButton(text="3")
    button_4 = types.KeyboardButton(text="4")
    keyboard = types.ReplyKeyboardMarkup(keyboard=[[button_1, button_2, button_3, button_4]], resize_keyboard=True)
    await message.answer("Сколько ключей?", reply_markup=keyboard)
    await state.set_state(CarState.keys)
