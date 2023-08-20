from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:
    def __init__(self, model):
        # db модель
        self.model = model

    # Метод сохранения объекта в базу
    @staticmethod
    async def save(session: AsyncSession, db_obj):
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    # Одинаковый для всех моделей метод GET по id
    async def get(self, obj_id: int, session: AsyncSession):
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    # Одинаковый для всех моделей метод GET всех записей
    async def get_many(self, session: AsyncSession):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    # Одинаковый для всех моделей метод CREATE
    async def create(
        self, obj_to_write, session: AsyncSession,
        user: Optional[User] = None
    ):
        # словарь из объекта pydantic модели
        obj_to_write_data = obj_to_write.dict()
        if user:
            obj_to_write_data['user_id'] = user.id
        db_obj = self.model(**obj_to_write_data)
        return await self.save(session, db_obj)

    async def update(
        self, db_obj, obj_to_update, session: AsyncSession
    ):
        # словарь из объекта бд
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_to_update.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        return await self.save(session, db_obj)

    @staticmethod
    async def remove(db_obj, session: AsyncSession):
        await session.delete(db_obj)
        await session.commit()
        return db_obj