from datetime import datetime
from typing import Union, List

from app.models import CharityProject, Donation


def fully_invested(
    obj: Union[CharityProject, Donation]
) -> Union[CharityProject, Donation]:
    """
    Переводит проет или донат в состояние "полной оплаты",
    т.е. обрабатывает события: все деньги доната ушли на проекты,
    либо вся необходимаю сумма для проекта собрана
    """
    obj.invested_amount = obj.full_amount
    obj.fully_invested = True
    obj.close_date = datetime.now()
    return obj


def make_recalculation(
    sources: Union[List[CharityProject], List[Donation]],
    target: Union[CharityProject, Donation]
) -> Union[List[CharityProject], List[Donation]]:
    """
    Универсальная функция для проведения перерасчетов при добавлении нового проекта или нового доната
    """
    modified_sources = []
    for source in sources:
        # остаток средств доната или недостающая сумма проекта
        exists_amount = source.full_amount - source.invested_amount
        # остаток средст НОВОГО доната или оставшаяся недостающая сумма НОВОГО проекта
        new_item_amount = target.full_amount - target.invested_amount

        # если рамер новых/оставшихся пожертвований точно соответствует
        # необходимой сумме на новые/имеющиеся проекты
        if exists_amount == new_item_amount:
            modified_sources.append(fully_invested(source))
            fully_invested(target)
            break
        # если размер оставшихся средств доната больше необходимой суммы на новый проект
        # либо оставшаяся необходимая сумма проекта больше суммы нового доната
        elif exists_amount > new_item_amount:
            source.invested_amount += new_item_amount
            fully_invested(target)
            break
        # если размер оставшихся средств доната меньше необходимой суммы на новый проект
        # либо оставшаяся необходимая сумма проекта меньше суммы нового доната
        else:
            target.invested_amount += exists_amount
            modified_sources.append(fully_invested(source))
    return modified_sources
