from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import Config
from database import Database
from handlers.users import CustomUserHandlers

bot = Bot(token=Config.token)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)


def main():
    try:
        data = Database()
        data.create_base()
        data.generate_product()
        CustomUserHandlers(bot, dp)

        executor.start_polling(dp, skip_updates=True)
    finally:
        pass


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped')
