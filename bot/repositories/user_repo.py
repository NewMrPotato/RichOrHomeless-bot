import datetime
from sqlalchemy.future import select
from database.models import UserWealth


class UserRepo:
    def __init__(self, session):
        self.session = session


    async def get_by_telegram_id(self, tg_id: int):
        q = await self.session.execute(select(UserWealth).where(UserWealth.telegram_id == tg_id))
        return q.scalars().first()


    async def create_or_update(self, tg_id: int, capital: float):
        instance = await self.get_by_telegram_id(tg_id)
        now = datetime.datetime.utcnow()
        if instance:
            instance.capital = capital
            instance.assigned_at = now
        else:
            instance = UserWealth(telegram_id=tg_id, capital=capital, assigned_at=now)
            self.session.add(instance)
        await self.session.commit()
        return instance


    async def set_capital_if_absent_or_expired(self, tg_id: int, capital_generator):
        import datetime
        inst = await self.get_by_telegram_id(tg_id)
        now = datetime.datetime.utcnow()
        if inst:
            diff = now - inst.assigned_at
            if diff.total_seconds() >= 24*3600:
                # expired -> regenerate
                inst.capital = await capital_generator(tg_id)
                inst.assigned_at = now
                await self.session.commit()
            return inst
        else:
            cap = await capital_generator(tg_id)
            return await self.create_or_update(tg_id, cap)