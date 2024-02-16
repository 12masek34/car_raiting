from aiogram import (
    F,
    Router,
    types,
)
from aiogram.filters import (
    Command,
)

from database.connection import (
    Db,
)

router = Router()


@router.message(F.text.lower().in_({"передний", "задний", "полный"}))
async def answer_drive_type(message: types.Message, db: Db):
    user_id = message.from_user.id
    drive_type = message.text
    await db.add_drive_type(user_id, drive_type)
    await message.answer(
        "Сделать Фото СТС или ПТС с читаемыми данными. Без бликов и размытости.",
        reply_markup=types.ReplyKeyboardRemove(),
    )


@router.message(F.text.lower().in_({"отсутствует", "зимняя", "летняя", "грязевая"}))
async def answer_tires(message: types.Message, db: Db):
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


@router.message(F.text.in_({"1", "2", "3", "4"}))
async def answer_keys(message: types.Message, db: Db):
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


@router.message(F.text.lower().in_({"да", "нет"}))
async def answer_restriction(message: types.Message, db: Db):
    user_id = message.from_user.id
    restricion = True if message.text.lower() == "да" else False
    await db.add_restriction(user_id, restricion)
    button_1 = types.KeyboardButton(text="1")
    button_2 = types.KeyboardButton(text="2")
    button_3 = types.KeyboardButton(text="3")
    button_4 = types.KeyboardButton(text="4")
    keyboard = types.ReplyKeyboardMarkup(keyboard=[[button_1, button_2, button_3, button_4]], resize_keyboard=True)
    await message.answer("Сколько ключей?", reply_markup=keyboard)


@router.message(Command("start"))
async def cmd_start(message: types.Message, db: Db):
    user_id = message.from_user.id
    await db.add_car(user_id)
    button_yes = types.KeyboardButton(text="да")
    button_no = types.KeyboardButton(text="нет")
    keyboard = types.ReplyKeyboardMarkup(keyboard=[[button_yes, button_no]], resize_keyboard=True)
    await message.answer("Есть ли текущий залог или ограничение на авто?", reply_markup=keyboard)
