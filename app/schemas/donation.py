from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic.types import PositiveInt


# Базовый класс для Pydantic-схем пожертвований
class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]


# Pydantic-схема для записи объекта пожертвования в базу
class DonationCreate(DonationBase):
    pass


# Pydantic-схема, описывающая объект пожертвования,
# возвращаемый из базы данных
class DonationDB(DonationBase):
    id: int
    create_date: datetime
    user_id: Optional[int]
    invested_amount: Optional[int]
    fully_invested: bool
    close_date: Optional[datetime]

    class Config:
        # для сериализации объекта ORM-модели в Pydantic-схему
        orm_mode = True
