from aiogram import (
    Bot,
    F,
    Router,
    types,
)
from aiogram.filters import (
    Command,
)
from aiogram.fsm.context import (
    FSMContext,
)

from config import (
    GROUP_ID,
)
from constants import (
    final,
    input_photo_phrase,
)
from database.connection import (
    Db,
)
from states import (
    CarState,
)
from utils import (
    get_pictures,
    get_summary,
)


router = Router()


@router.message(Command("start"))
@router.message(F.text.lower() == "start")
async def cmd_start(message: types.Message, state: FSMContext, db: Db):
    user_id = message.from_user.id
    await db.add_car(user_id)
    button_yes = types.KeyboardButton(text="Да")
    button_no = types.KeyboardButton(text="Нет")
    keyboard = types.ReplyKeyboardMarkup(keyboard=[[button_yes, button_no]], resize_keyboard=True)
    await message.answer("Есть ли текущий залог или ограничение на авто?", reply_markup=keyboard)
    await state.set_state(CarState.restriction)


@router.message(F.text.lower() == final.lower())
async def finish(message: types.Message, state: FSMContext, db: Db, bot: Bot):
    user_id = message.from_user.id
    pics, docs = await db.get_documents(user_id)
    summary = await db.get_summary(user_id)
    summary_answer = get_summary(pics, docs, summary)
    button_start = types.KeyboardButton(text="start")
    keyboard = types.ReplyKeyboardMarkup(keyboard=[[button_start]], resize_keyboard=True)

    for answer in summary_answer:
        await bot.send_media_group(GROUP_ID, answer)

    await message.answer("Жми старт!", reply_markup=keyboard)


@router.message(CarState.car_photo_8)
async def car_photo_8(message: types.Message, state: FSMContext, db: Db):
    document_id = getattr(message.document, "file_id", None)
    photo_id = getattr(message.photo[-1], "file_id", None) if message.photo else None
    user_id = message.from_user.id
    button_finish = types.KeyboardButton(text=final)
    keyboard = types.ReplyKeyboardMarkup(keyboard=[[button_finish]], resize_keyboard=True)
    await db.add_document(user_id, document_id, photo_id)
    await message.answer(
        "Пофоткай очевидные повреждения/дефекты кузова/салона если такие есть.",
        reply_markup=keyboard,
    )
    await state.set_state(CarState.car_photo_8)


@router.message(CarState.car_photo_7)
async def car_photo_7(message: types.Message, state: FSMContext, db: Db):
    document_id = getattr(message.document, "file_id", None)
    photo_id = getattr(message.photo[-1], "file_id", None) if message.photo else None
    user_id = message.from_user.id
    photo_rear_seat = get_pictures("rear_seat.jpg")
    await db.add_document(user_id, document_id, photo_id)
    await message.answer_photo(photo_rear_seat)
    await message.answer(input_photo_phrase)
    await state.set_state(CarState.car_photo_8)


@router.message(CarState.car_photo_6)
async def car_photo_6(message: types.Message, state: FSMContext, db: Db):
    document_id = getattr(message.document, "file_id", None)
    photo_id = getattr(message.photo[-1], "file_id", None) if message.photo else None
    user_id = message.from_user.id
    photo_front_seat = get_pictures("front_seat.jpg")
    await db.add_document(user_id, document_id, photo_id)
    await message.answer_photo(photo_front_seat)
    await message.answer(input_photo_phrase)
    await state.set_state(CarState.car_photo_7)


@router.message(CarState.car_photo_5)
async def car_photo_5(message: types.Message, state: FSMContext, db: Db):
    document_id = getattr(message.document, "file_id", None)
    photo_id = getattr(message.photo[-1], "file_id", None) if message.photo else None
    user_id = message.from_user.id
    photo_selector = get_pictures("selector.jpg")
    await db.add_document(user_id, document_id, photo_id)
    await message.answer_photo(photo_selector)
    await message.answer(input_photo_phrase)
    await state.set_state(CarState.car_photo_6)


@router.message(CarState.car_photo_4)
async def car_photo_4(message: types.Message, state: FSMContext, db: Db):
    document_id = getattr(message.document, "file_id", None)
    photo_id = getattr(message.photo[-1], "file_id", None) if message.photo else None
    user_id = message.from_user.id
    photo_panel = get_pictures("panel.jpg")
    await db.add_document(user_id, document_id, photo_id)
    await message.answer_photo(photo_panel)
    await message.answer(input_photo_phrase)
    await state.set_state(CarState.car_photo_5)


@router.message(CarState.car_photo_3)
async def car_photo_3(message: types.Message, state: FSMContext, db: Db):
    document_id = getattr(message.document, "file_id", None)
    photo_id = getattr(message.photo[-1], "file_id", None) if message.photo else None
    user_id = message.from_user.id
    photo_right = get_pictures("right.jpg")
    await db.add_document(user_id, document_id, photo_id)
    await message.answer_photo(photo_right)
    await message.answer(input_photo_phrase)
    await state.set_state(CarState.car_photo_4)


@router.message(CarState.car_photo_2)
async def car_photo_2(message: types.Message, state: FSMContext, db: Db):
    document_id = getattr(message.document, "file_id", None)
    photo_id = getattr(message.photo[-1], "file_id", None) if message.photo else None
    user_id = message.from_user.id
    photo_rear = get_pictures("rear.jpg")
    await db.add_document(user_id, document_id, photo_id)
    await message.answer_photo(photo_rear)
    await message.answer(input_photo_phrase)
    await state.set_state(CarState.car_photo_3)


@router.message(CarState.car_photo_1)
async def car_photo_1(message: types.Message, state: FSMContext, db: Db):
    document_id = getattr(message.document, "file_id", None)
    photo_id = getattr(message.photo[-1], "file_id", None) if message.photo else None
    user_id = message.from_user.id
    photo_front = get_pictures("left.jpg")
    await db.add_document(user_id, document_id, photo_id)
    await message.answer_photo(photo_front)
    await message.answer(input_photo_phrase)
    await state.set_state(CarState.car_photo_2)


@router.message(CarState.document_photo)
async def document(message: types.Message, state: FSMContext, db: Db):
    document_id = getattr(message.document, "file_id", None)
    photo_id = getattr(message.photo[-1], "file_id", None) if message.photo else None
    user_id = message.from_user.id
    photo_front = get_pictures("front.jpg")
    await db.add_document(user_id, document_id, photo_id)
    await message.answer_photo(photo_front)
    await message.answer(input_photo_phrase)
    await state.set_state(CarState.car_photo_1)


@router.message(CarState.driver_type)
async def drive_type(message: types.Message, state: FSMContext, db: Db):
    user_id = message.from_user.id
    drive_type = message.text
    photo_sts = get_pictures("sts.jpg")
    await db.add_drive_type(user_id, drive_type)
    await message.answer_photo(photo_sts)
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
    button_drive_type_front = types.KeyboardButton(text="Передний")
    button_drive_type_rear = types.KeyboardButton(text="Задний")
    button_drive_type_full = types.KeyboardButton(text="Полный")
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
    button_tire_disable = types.KeyboardButton(text="Отсутствует")
    button_tire_winter = types.KeyboardButton(text="Зимняя")
    button_tire_summer = types.KeyboardButton(text="Летняя")
    button_tire_mud = types.KeyboardButton(text="Грязевая")
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
