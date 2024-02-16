from aiogram import Router, types, F
from aiogram.filters import Command
from config import log
from database import queries
from database.connection import Db


router = Router()

@router.message(F.text.lower() == "да")
@router.message(F.text.lower() == "нет")
async def answer_yes(message: types.Message, db: Db):
    user_id = message.from_user.id
    restricion = True if message.text.lower() == "да" else False
    await db.add_restriction(user_id, restricion)
    await message.answer("Это здорово!", reply_markup=types.ReplyKeyboardRemove())


@router.message(Command("start"))
async def cmd_start(message: types.Message, db: Db):
    user_id = message.from_user.id
    await db.insert_car(user_id)
    button_yes = types.KeyboardButton(text="да")
    button_no = types.KeyboardButton(text="нет")
    keyboard = types.ReplyKeyboardMarkup(keyboard=[[button_yes, button_no]], resize_keyboard=True)
    await message.answer("Есть ли текущий залог или ограничение на авто?", reply_markup=keyboard)
