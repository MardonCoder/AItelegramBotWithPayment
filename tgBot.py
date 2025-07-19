import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import TOKEN, CLICK_TEST_TOKEN
from database import init_db, add_user, get_balance, update_balance, reset_balance
from AIscript import GPTChat

# Токен оплаты
payment_token = CLICK_TEST_TOKEN

# Логирование
logging.basicConfig(level=logging.INFO)

# Создание бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Инициализация OpenAI
chat_gpt = GPTChat()

# Курсы списания токенов
INPUT_TOKEN_COST = 3500 / 1_000_000  # 3 500 = 1 000 000 входных токенов
OUTPUT_TOKEN_COST = 15_000 / 1_000_000  # 15 000 = 1 000 000 выходных токенов
BALANCE_LIMIT = 750  # Минимальный баланс для запроса

keyBoard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/help"), KeyboardButton(text="/balance"), KeyboardButton(text="/pay")]
    ],
    resize_keyboard=True
)

paymentKeyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Назад")],
        [KeyboardButton(text="5000 сум"), KeyboardButton(text="10000 сум"), KeyboardButton(text="15000 сум")],
        [KeyboardButton(text="25000 сум")]
    ],
    resize_keyboard=True
)

payment_options = {
    "5000 сум": (5000, "testPayload5000"),
    "10000 сум": (10000, "testPayload10000"),
    "15000 сум": (15000, "testPayload15000"),
    "25000 сум": (25000, "testPayload25000"),
}

@dp.message(CommandStart())
async def start_command(message: types.Message):
    await add_user(message.from_user.id, message.from_user.username)
    await message.answer("""🙌 Привет, я — Scoopy, бот, который помогает СММ-специалистам работать эффективнее!😺

В данный момент я умею:

- Придумывать воронки продаж 🔼
- Писать описания для постов 📖
- Анализировать конкурентов 🙇‍♂️

💡 Напиши /help, чтобы узнать, как работать со мной. За это ты получишь 7 000 монет!""", reply_markup=keyBoard)

@dp.message(Command("help"))
async def help_command(message: types.Message):
    user_balance = await get_balance(message.from_user.id)
    if user_balance == 0:
        await update_balance(message.from_user.id, 7000)
        await message.answer("🎁 Вы получили 7 000 монет на баланс!")

    help_text = (
        """😃 Чтобы эффективнее использовать меня, опишите ваш запрос подробно, например:

1️⃣ Составь воронку продаж начиная с таргетированной рекламы для ниши "ваша ниша".
2️⃣ Дай совет по таргетированной рекламе: какой креатив лучше использовать, какое УТП лучше внедрить?

📌 Чем конкретнее вопрос, тем лучше ответ!"""
    )
    await message.answer(help_text)

@dp.message(Command("balance"))
async def balance_command(message: types.Message):
    balance = await get_balance(message.from_user.id)
    await message.answer(f"Ваш баланс: {balance} монет.")

@dp.message(Command("pay"))
async def start_paying(message: types.Message):
    await message.answer("На какую сумму вы хотите совершить оплату? (1 сум = 1 монета)", reply_markup=paymentKeyboard)

@dp.message(lambda message: message.text in payment_options)
async def send_invoice(message: types.Message):
    amount, payload = payment_options[message.text]
    await bot.send_invoice(
        chat_id=message.chat.id,
        title=f"Покупка за {amount}",
        description=f"Оплата за {amount} сум",
        payload=payload,
        provider_token=payment_token,
        currency="UZS",
        prices=[types.LabeledPrice(label="Оплата", amount=amount * 100)],
        start_parameter="payment",
        is_flexible=False
    )

@dp.message(lambda message: message.text == "Назад")
async def go_back(message: types.Message):
    await message.answer("Вы вернулись в основное меню.", reply_markup=keyBoard)

@dp.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message(lambda message: message.successful_payment is not None)
async def process_successful_payment(message: types.Message):
    amount = message.successful_payment.total_amount // 100
    payload = message.successful_payment.invoice_payload
    for pay_sum, (sum_amount, pay_payload) in payment_options.items():
        if payload == pay_payload:
            await update_balance(message.from_user.id, sum_amount)
            break

    new_balance = await get_balance(message.from_user.id)
    await message.answer(f"✅ Оплата {amount} UZS прошла успешно!\n💰 Ваш новый баланс: {new_balance} монет.")

"""Работа ИИ бота"""
@dp.message(lambda message: message.text is not None)
async def ai_response(message: types.Message):
    """Обработка сообщений и списание токенов"""
    user_balance = await get_balance(message.from_user.id)

    if user_balance < BALANCE_LIMIT:
        await message.answer("❌ Недостаточно средств! Пополните баланс минимум до 750 монет.")
        return

    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")

    response = await chat_gpt.chat(message.text)

    # Парсим количество использованных токенов
    try:
        answer, tokens_text = response.rsplit("\n\n🔹", 1)
        tokens_used = int(tokens_text.split(":")[1].strip())

        # Рассчитываем стоимость запроса
        input_cost = tokens_used * INPUT_TOKEN_COST
        output_cost = tokens_used * OUTPUT_TOKEN_COST
        total_cost = round(input_cost + output_cost)

        # Проверяем баланс перед списанием
        if user_balance < total_cost:
            await message.answer(f"❌ Недостаточно средств! Стоимость запроса: {total_cost} монет.")
            return

        # Списываем токены
        await update_balance(message.from_user.id, -total_cost)
        new_balance = await get_balance(message.from_user.id)

        await message.answer(f"{answer}\n\n💰 Списано: {total_cost} монет.\n🔹 Остаток: {new_balance} монет.")

    except Exception as e:
        logging.error(f"Ошибка при обработке токенов: {e}")
        await message.answer("Ошибка при обработке запроса. Попробуйте позже.")

async def main():
    logging.info("Бот запущен...")
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен вручную.")
    except Exception as e:
        logging.error(f"Ошибка при запуске бота: {e}")
