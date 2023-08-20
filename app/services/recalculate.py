from datetime import datetime
from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import false

from app.models import CharityProject, Donation


async def fully_invested(session: AsyncSession, obj: Union[CharityProject, Donation]) -> None:
    """
    Переводит проет или донат в состояние "полной оплаты",
    т.е. обрабатывает события: все деньги доната ушли на проекты,
    либо вся необходимаю сумма для проекта собрана
    """
    obj.invested_amount = obj.full_amount
    obj.fully_invested = True
    obj.close_date = datetime.now()
    session.add(obj)


async def make_recalculation(
    session: AsyncSession, new_item: Union[CharityProject, Donation]
) -> Union[CharityProject, Donation]:
    """
    Универсальная функция для проведения перерасчетов при добавлении нового проекта или нового доната
    """
    search_model = Donation if isinstance(new_item, CharityProject) else CharityProject
    all_active_items = await session.execute(
        select(search_model).where(
            search_model.fully_invested == false()
        ).order_by(search_model.create_date)
    )

    for active_item in all_active_items.scalars().all():
        # остаток средств доната или недостающая сумма проекта
        exists_amount = active_item.full_amount - active_item.invested_amount
        # остаток средст НОВОГО доната или оставшаяся недостающая сумма НОВОГО проекта
        new_item_amount = new_item.full_amount - new_item.invested_amount

        # если рамер новых/оставшихся пожертвований точно соответствует
        # необходимой сумме на новые/имеющиеся проекты
        if exists_amount == new_item_amount:
            await fully_invested(session, active_item)
            await fully_invested(session, new_item)
            break
        # если размер оставшихся средств доната больше необходимой суммы на новый проект
        # либо оставшаяся необходимая сумма проекта больше суммы нового доната
        elif exists_amount > new_item_amount:
            active_item.invested_amount += new_item_amount
            await fully_invested(session, new_item)
            break
        # если размер оставшихся средств доната меньше необходимой суммы на новый проект
        # либо оставшаяся необходимая сумма проекта меньше суммы нового доната
        else:
            new_item.invested_amount += exists_amount
            await fully_invested(session, active_item)
    await session.commit()
    await session.refresh(new_item)
    return new_item
