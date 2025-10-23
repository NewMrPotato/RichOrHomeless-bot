from aiogram import F
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from aiogram import Router
from bot.factories import get_bot
from database.session import AsyncSessionLocal
from bot.repositories.user_repo import UserRepo
from bot.services.wealth_service import generate_capital, pick_phrase_and_emoji
import asyncio
import uuid


router = Router()


async def register_inline_handlers(dp):
    dp.include_router(router)




@router.inline_query()
async def inline_wealth(query: InlineQuery):
    # Будем отвечать на любой inline-запрос к боту (например: @BotUsername)
    # query.from_user.id — telegram id
    user = query.from_user
    tg_id = user.id


    # Получаем/создаём сессию и репозиторий
    async with AsyncSessionLocal() as session:
        repo = UserRepo(session)


        async def capital_generator(uid: int):
            return await generate_capital(uid)


        record = await repo.set_capital_if_absent_or_expired(tg_id, capital_generator)
        cap = record.capital


    phrase, emoji = pick_phrase_and_emoji(cap)


    text = f"{phrase}, у меня состояние ${cap:,.2f} {emoji}"


    result = InlineQueryResultArticle(
        id=str(uuid.uuid4()),
        #title=f"Твой капитал: ${cap:,.2f}",
        title=f"Узнай своё финансовое положение 👀",
        input_message_content=InputTextMessageContent(message_text=text)
    )


    await query.answer(results=[result], cache_time=0) # cache_time=0 чтобы результат быстро менялся для формулировок