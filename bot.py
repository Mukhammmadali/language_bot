from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

API_TOKEN = '6786137795:AAGNZuiN5WBQd0cDBIkt5D6dfDODg-Xualc'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


questions_en = [
    {"question": "Translate to English: 'дом'", "answer": "uy"},
    {"question": "Translate to English: 'кошка'", "answer": "mushuk"},
]

questions_ru = [
    {"question": "Переведите на русский: 'kuchuk'", "answer": "собака"},
    {"question": "Переведите на русский: 'kitob'", "answer": "книга"},
]

user_data = {}


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["English", "Russian"]
    keyboard.add(*buttons)
    await message.answer("Salom! Men o'qituvchi botman. Qaysi tilni o'rganishni istaysiz?", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text in ["English", "Russian"])
async def set_language(message: types.Message):
    user_data[message.from_user.id] = {
        "language": message.text,
        "question_index": 0
    }

    if message.text == "English":
        question = questions_en[0]['question']
    else:
        question = questions_ru[0]['question']

    await message.answer(f"{message.text} tilini o'rganishni boshlaymiz. Birinchi savol:")
    await message.answer(question)


@dp.message_handler(lambda message: message.from_user.id in user_data)
async def handle_answer(message: types.Message):
    user_id = message.from_user.id
    language = user_data[user_id]["language"]
    index = user_data[user_id]["question_index"]

    if language == "English":
        correct_answer = questions_en[index]['answer']
    else:
        correct_answer = questions_ru[index]['answer']

    if message.text.lower() == correct_answer.lower():
        await message.answer("To'g'ri javob!")
    else:
        await message.answer(f"Noto'g'ri javob. To'g'ri javob: {correct_answer}")

    user_data[user_id]["question_index"] += 1
    index = user_data[user_id]["question_index"]

    if (language == "English" and index < len(questions_en)) or (language == "Russian" and index < len(questions_ru)):
        if language == "English":
            question = questions_en[index]['question']
        else:
            question = questions_ru[index]['question']
        await message.answer(question)
    else:
        await message.answer("Savollar tugadi! /start komandasini yuborib qayta boshlashingiz mumkin.")
        user_data.pop(user_id)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
