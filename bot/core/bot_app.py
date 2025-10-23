import asyncio
from bot.factories import get_bot, get_dispatcher
from bot.handlers.inline import register_inline_handlers


async def start():
    bot = get_bot()
    dp = get_dispatcher(bot)


    await register_inline_handlers(dp)


    try:
        print('Long polling started...')
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())