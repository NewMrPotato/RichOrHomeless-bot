from sqlalchemy import Column, Integer, BigInteger, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime


Base = declarative_base()


class UserWealth(Base):
    __tablename__ = 'user_wealth'


    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True, nullable=False)
    capital = Column(Float, nullable=False)
    assigned_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
