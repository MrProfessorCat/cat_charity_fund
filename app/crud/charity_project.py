from typing import Dict, List, Optional, Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, true

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):
    async def get_projects_by_completion_rate(
        self, session: AsyncSession
    ) -> List[Dict[str, Union[Optional[str], int]]]:
        SECONDS_IN_DAY = 86_400
        projects = await session.execute(
            select(
                [
                    CharityProject.name,
                    func.round((
                        func.julianday(CharityProject.close_date) -
                        func.julianday(CharityProject.create_date)
                    ) * SECONDS_IN_DAY).label('timedelta'),
                    CharityProject.description
                ]
            ).where(
                CharityProject.fully_invested == true()
            ).order_by(
                (
                    func.julianday(CharityProject.close_date) -
                    func.julianday(CharityProject.create_date)
                ) * SECONDS_IN_DAY
            )
        )
        return projects.all()


charity_project_crud = CRUDCharityProject(CharityProject)
