import aiosqlite
import asyncio


async def show_db_contents(db_path):
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = await cursor.fetchall()

        if not tables:
            print("База данных пуста или не содержит таблиц.")
            return

        for (table_name,) in tables:
            print(f"\nСодержимое таблицы: {table_name}")
            cursor = await db.execute(f"SELECT * FROM {table_name}")
            rows = await cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            print(" | ".join(columns))
            print("-" * 40)
            for row in rows:
                print(" | ".join(map(str, row)))

            await cursor.close()


if __name__ == "__main__":
    db_file = "users.db"  # Укажите путь к вашему .db файлу
    asyncio.run(show_db_contents(db_file))
