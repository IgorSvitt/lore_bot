from database_all_tables import Database
import asyncio
from bot_telegram import bot


db = Database()


async def main() -> None:
    await db.create_tables()
    await bot.polling(none_stop=True)


if __name__ == '__main__':
    asyncio.run(main())
