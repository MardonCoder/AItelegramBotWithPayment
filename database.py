import aiosqlite
from config import DB_NAME

async def init_db():
    """Создание таблицы пользователей при старте бота."""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                balance INTEGER DEFAULT 0
            )
        """)
        await db.commit()

async def add_user(user_id: int, username: str | None):
    """Добавить пользователя в базу, если его ещё нет."""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)
        """, (user_id, username))
        await db.commit()

async def get_balance(user_id: int) -> int:
    """Получить баланс пользователя."""
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0

async def update_balance(user_id: int, amount: int):
    """Обновить баланс пользователя."""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
        await db.commit()

async def reset_balance(user_id: int):
    """Сбросить баланс пользователя."""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE users SET balance = 0 WHERE user_id = ?", (user_id, ))
        await db.commit()