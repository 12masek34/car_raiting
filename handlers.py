from aiogram import (
    Bot,
    F,
    Router,
    types,
)
from aiogram.enums.parse_mode import (
    ParseMode,
)
from aiogram.filters import (
    Command,
)
from aiogram.fsm.context import (
    FSMContext,
)

from config import (
    GROUP_ID,
    log,
)
from constants import (
    btn_driver_type,
    btn_keys,
    btn_tire,
    btn_yes_no,
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
    get_keyboard,
    get_pictures,
    get_summary,
)


router = Router()


@router.message(Command("start"))
@router.message(F.text.lower() == "start")
async def cmd_start(message: types.Message, state: FSMContext, db: Db):
    user_id = message.from_user.id
    user_name = message.from_user.username
    log.info(f" Пользователь user_id={user_id} user_name={user_name} стартует бота")
    await db.add_car(user_id)
    keyboard = get_keyboard(*btn_yes_no)
    await message.answer("Есть ли текущий залог или ограничение на авто?", reply_markup=keyboard)
    await state.set_state(CarState.restriction)


@router.message(F.text.lower() == final.lower())
async def finish(message: types.Message, db: Db, bot: Bot):
    user_id = message.from_user.id
    user_name = message.from_user.username
    log.info(f" Пользователь user_id={user_id} user_name={user_name} закончил принимать тачку")
    pics, docs = await db.get_documents(user_id)
    summary = await db.get_summary(user_id)
    summary_answer = get_summary(pics, docs, summary)
    keyboard = get_keyboard("start")

    for answer in summary_answer:
        await bot.send_media_group(GROUP_ID, answer)

    await message.answer("Жми старт!", reply_markup=keyboard)


@router.message(CarState.car_photo_8)
async def car_photo_8(message: types.Message, state: FSMContext, db: Db):
    document_id = getattr(message.document, "file_id", None)
    photo_id = getattr(message.photo[-1], "file_id", None) if message.photo else None
    user_id = message.from_user.id
    user_name = message.from_user.username
    log.info(f" Пользователь user_id={user_id} user_name={user_name} добавил 8 фото")
    keyboard = get_keyboard(final)
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
    user_name = message.from_user.username
    log.info(f" Пользователь user_id={user_id} user_name={user_name} добавил 7 фото")
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
    user_name = message.from_user.username
    log.info(f" Пользователь user_id={user_id} user_name={user_name} добавил 6 фото")
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
    user_name = message.from_user.username
    log.info(f" Пользователь user_id={user_id} user_name={user_name} добавил 5 фото")
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
    user_name = message.from_user.username
    log.info(f" Пользователь user_id={user_id} user_name={user_name} добавил 4 фото")
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
    user_name = message.from_user.username
    log.info(f" Пользователь user_id={user_id} user_name={user_name} добавил 3 фото")
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
    user_name = message.from_user.username
    log.info(f" Пользователь user_id={user_id} user_name={user_name} добавил 2 фото")
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
    user_name = message.from_user.username
    log.info(f" Пользователь user_id={user_id} user_name={user_name} добавил 1 фото")
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
    user_name = message.from_user.username
    log.info(f" Пользователь user_id={user_id} user_name={user_name} добвил фото документов")
    photo_front = get_pictures("front.jpg")
    await db.add_document(user_id, document_id, photo_id)
    await message.answer_photo(photo_front)
    await message.answer(input_photo_phrase)
    await state.set_state(CarState.car_photo_1)


@router.message(CarState.driver_type)
async def drive_type(message: types.Message, state: FSMContext, db: Db):
    document_id = getattr(message.document, "file_id", None)
    photo_id = getattr(message.photo[-1], "file_id", None) if message.photo else None

    if document_id or photo_id:
        keyboard = get_keyboard(*btn_driver_type)
        await message.answer("Непонял, какой привод на авто?", reply_markup=keyboard)
        await state.set_state(CarState.driver_type)
        return

    user_id = message.from_user.id
    user_name = message.from_user.username
    log.info(f" Пользователь user_id={user_id} user_name={user_name} добавил тип привода авто")
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
    document_id = getattr(message.document, "file_id", None)
    photo_id = getattr(message.photo[-1], "file_id", None) if message.photo else None

    if document_id or photo_id:
        keyboard = get_keyboard(*btn_tire)
        await message.answer("Непонял, есть ли доп. комплект резины?", reply_markup=keyboard)
        await state.set_state(CarState.tires)
        return

    user_id = message.from_user.id
    user_name = message.from_user.username
    tire = message.text
    log.info(f" Пользователь user_id={user_id} user_name={user_name} добавил шины")

    await db.add_tire(user_id, tire)
    keyboard = get_keyboard(*btn_driver_type)
    await message.answer("Какой привод на авто?", reply_markup=keyboard)
    await state.set_state(CarState.driver_type)


@router.message(CarState.keys)
async def keys(message: types.Message, state: FSMContext, db: Db):
    document_id = getattr(message.document, "file_id", None)
    photo_id = getattr(message.photo[-1], "file_id", None) if message.photo else None

    if document_id or photo_id:
        keyboard = get_keyboard(*btn_keys)
        await message.answer(
            "Непонял, сколько ключей?\nВведи число\.",
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        await state.set_state(CarState.keys)
        return

    text = message.text or ""

    if not text.isdigit():
        keyboard = get_keyboard(*btn_keys)
        await message.answer(
            "Непонял, сколько ключей?\nВведи число\.",
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        await state.set_state(CarState.keys)
        return

    user_id = message.from_user.id
    user_name = message.from_user.username
    log.info(f" Пользователь user_id={user_id} user_name={user_name} добавил количество ключей")
    number_of_keys = int(text) if message.text.isdigit() else None
    await db.add_number_of_keys(user_id, number_of_keys)
    keyboard = get_keyboard(*btn_tire)
    await message.answer("Есть ли доп. комплект резины?", reply_markup=keyboard)
    await state.set_state(CarState.tires)


@router.message(CarState.restriction)
async def restriction(message: types.Message, state: FSMContext, db: Db):
    document_id = getattr(message.document, "file_id", None)
    photo_id = getattr(message.photo[-1], "file_id", None) if message.photo else None

    if document_id or photo_id:
        keyboard = get_keyboard(*btn_yes_no)
        await message.answer(
            "Непонял, есть ли текущий залог или ограничение на авто?\nда или нет?",
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        await state.set_state(CarState.restriction)
        return

    text = message.text.lower()

    if text not in [key.lower() for key in btn_yes_no]:
        keyboard = get_keyboard(*btn_yes_no)
        await message.answer(
            "Непонял, есть ли текущий залог или ограничение на авто?\nда или нет?",
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        await state.set_state(CarState.restriction)
        return

    user_id = message.from_user.id
    user_name = message.from_user.username
    log.info(f" Пользователь user_id={user_id} user_name={user_name} добавил ограничение")
    restricion = True if text == "да" else False
    await db.add_restriction(user_id, restricion)
    keyboard = get_keyboard(*btn_keys)
    await message.answer("Сколько ключей?", reply_markup=keyboard)
    await state.set_state(CarState.keys)
