from app.crud import charity_project_crud, donation_crud
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def invest_in_projects(session: AsyncSession):
    open_projects = await charity_project_crud.get_uninvested_charity_projects(session)

    for project in open_projects:
        remaining_amount = project.full_amount - project.invested_amount
        free_donations = await donation_crud.get_uninvested_donations(session)
        temp_project = CharityProject(**project.dict())

        for donation in free_donations:
            if remaining_amount == 0:
                break

            temp_donation = Donation(**donation.dict())
            if temp_donation.invested_amount < temp_donation.full_amount:
                investment_amount = min(
                    remaining_amount,
                    temp_donation.full_amount - temp_donation.invested_amount,
                )
                temp_project.invested_amount += investment_amount
                temp_donation.invested_amount += investment_amount
                remaining_amount -= investment_amount

                if temp_project.invested_amount == temp_project.full_amount:
                    temp_project.fully_invested = True
                    temp_project.close_date = datetime.utcnow()

                if temp_donation.invested_amount == temp_donation.full_amount:
                    temp_donation.fully_invested = True

                await donation_crud.update(donation, temp_donation, session)

        await charity_project_crud.update(project, temp_project, session)

    await session.commit()
