import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
import config
from handlers.users.menu import router as menu_router




async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_router(menu_router)

    # And the run events dispatching
    await dp.start_polling(bot)

if __name__ == "__main__":

    asyncio.run(main())