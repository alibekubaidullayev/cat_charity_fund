from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.models import User


class CRUDDonation(CRUDBase):
    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(Donation.id).where(Donation.name == project_name)
        )
        return db_project_id.scalars().first()

    async def get_uninvested_donations(self, session: AsyncSession) -> list[Donation]:
        uninvested_donations = await session.execute(
            select(Donation)
            .where(Donation.fully_invested == False)
            .order_by(Donation.create_date)
        )
        return uninvested_donations.scalars().all()


donation_crud = CRUDDonation(Donation)
