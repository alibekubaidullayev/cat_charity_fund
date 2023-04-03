from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject

from .donation import donation_crud


class CRUDCharityProject(CRUDBase):
    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(CharityProject.name == project_name)
        )
        return db_project_id.scalars().first()

    async def get_uninvested_charity_projects(self, session: AsyncSession):
        uninvested_donations = await session.execute(
            select(CharityProject)
            .where(CharityProject.fully_invested == False)
            .order_by(CharityProject.create_date)
        )

        return uninvested_donations.scalars()


charity_project_crud = CRUDCharityProject(CharityProject)
