from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_exists, check_project_is_closed,
    check_new_amount_larger_then_invested, check_if_invested,
    check_name_duplicate
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)
from app.services.recalculate import make_recalculation


router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    await check_name_duplicate(charity_project.name, session)
    new_charity_project = await charity_project_crud.create(charity_project, session)
    moidified_sources = make_recalculation(
        await donation_crud.get_all_active(session),
        new_charity_project
    )
    session.add_all(moidified_sources)
    return await charity_project_crud.save(session, new_charity_project)


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    return await charity_project_crud.get_many(session)


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def update_charity_project(
    charity_project_id: int,
    charity_project_in_request: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    charity_project = await check_charity_project_exists(charity_project_id, session)
    await check_project_is_closed(charity_project)
    await check_new_amount_larger_then_invested(charity_project_in_request, charity_project)
    await check_name_duplicate(charity_project_in_request.name, session)
    return await charity_project_crud.update(
        charity_project, charity_project_in_request, session
    )


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def delete_charity_project(
    charity_project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    charity_project = await check_charity_project_exists(charity_project_id, session)
    await check_if_invested(charity_project)
    return await charity_project_crud.remove(charity_project, session)
