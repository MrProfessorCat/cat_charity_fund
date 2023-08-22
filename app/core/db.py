from datetime import datetime

from sqlalchemy import CheckConstraint, Column, Integer, DateTime, Boolean
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from app.core.config import settings


class PreBase:
    @declared_attr
    def __tablename__(cls):
        # имя таблицы = имя модели
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


# базовый класс для будущих моделей
Base = declarative_base(cls=PreBase)


class ABCBase(Base):
    __abstract__ = True
    __table_args__ = (
        CheckConstraint(
            '0 <= invested_amount AND invested_amount <= full_amount'
        ),
    )

    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)


# движок бд
engine = create_async_engine(settings.database_url)

# для асинхронной работы - множественное создание сессий
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session
