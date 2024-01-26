
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
import asyncio
from core.utils.settings import Settings
from core.hendlers.basic import get_start, change_href, get_href, litl_chang
from aiogram.utils.markdown import hlink
from core.filtrs.isThisHref import FilterLinks
from aiogram.filters import Command
from core.utils.States import Stateses


async def start():

    bot = Bot(Settings.bots.bot_token)
    dp = Dispatcher()

    dp.message.register(get_start, Command(commands=['start']))
    dp.message.register(get_href, Stateses.INPUT_HREF)
    dp.message.register(litl_chang)


    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(start())


