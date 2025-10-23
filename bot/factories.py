from aiogram import Bot, Dispatcher
from bot.settings import settings


_bot = None
_dp = None


def get_bot():
    global _bot
    if not _bot:
        _bot = Bot(token=settings.BOT_TOKEN, parse_mode='HTML')
    return _bot


def get_dispatcher(bot=None):
    global _dp
    if not _dp:
        from aiogram.fsm.storage.memory import MemoryStorage
        _dp = Dispatcher(storage=MemoryStorage())
    return _dp