from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_charity_project_exists(
    charity_project_id: int,
    session: AsyncSession
) -> CharityProject:
    charity_project = await charity_project_crud.get(charity_project_id, session)
    if not charity_project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return charity_project


async def check_project_is_closed(
    charity_project: CharityProject
) -> None:
    """
    Если проект уже закрыт, изменять его нельзя
    """
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )


async def check_new_amount_larger_then_invested(
    charity_project_in_request: CharityProjectUpdate,
    charity_project: CharityProject
) -> None:
    """
    Если в проект вносится измение суммы,
    то новая сумма не может быть меньше уже внесенной
    """
    if (
        charity_project_in_request.full_amount and
        charity_project_in_request.full_amount < charity_project.invested_amount
    ):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя указывать сумму проекта меньше внесенной в него суммы!'
        )


async def check_if_invested(
    charity_project: CharityProject
) -> None:
    """
    Запрещено удалять проект, если в него были внесены какие-то средства
    """
    if charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


async def check_name_duplicate(
    charity_project_name: str,
    session: AsyncSession
) -> None:
    """
    Не должно быть два проекта с одинаковыми именами
    """
    if charity_project_name:
        charity_project = await charity_project_crud.get_charity_project_by_name(
            charity_project_name, session
        )
        if charity_project:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Проект с таким именем уже существует!'
            )