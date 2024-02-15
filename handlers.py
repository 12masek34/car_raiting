from aiogram import Router, types, F



router = Router()

@router.message(F.text.lower() == "да")
@router.message(F.text.lower() == "нет")
async def answer_yes(message: types.Message):

    button = types.KeyboardButton(text="Старт")
    keyboard = types.ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True)
    await message.answer(
        "Это здорово!",
        reply_markup=keyboard
    )

@router.message()
async def cmd_start(message: types.Message):
    print(message.text)
    button_yes = types.KeyboardButton(text="да")
    button_no = types.KeyboardButton(text="нет")
    keyboard = types.ReplyKeyboardMarkup(keyboard=[[button_yes, button_no]], resize_keyboard=True)
    await message.answer("Есть ли текущий залог или ограничение на авто?", reply_markup=keyboard)

