from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud, donation_crud


async def invest_project(project, session: AsyncSession):
    while not project.fully_invested:
        donation = await donation_crud.get_uninvested_donation(session)

        if not donation:
            return project

        modified_project, _ = await invest_in_project(project, donation, session)

    return modified_project


async def invest_donation(donation, session: AsyncSession):
    while not donation.fully_invested:
        project = await charity_project_crud.get_uninvested_charity_project(session)

        if not project:
            return donation

        _, modified_donation = await invest_in_project(project, donation, session)

    return modified_donation


async def invest_in_project(project, donation, session: AsyncSession):
    available_amount = donation.full_amount - donation.invested_amount

    if available_amount == 0:
        return project, donation

    if project.invested_amount + available_amount <= project.full_amount:
        project.invested_amount += available_amount
        donation.invested_amount += available_amount
        donation.fully_invested = True
        donation.close_date = datetime.now()
    else:
        required_amount = project.full_amount - project.invested_amount
        donated_amount = min(required_amount, available_amount)

        project.invested_amount += donated_amount
        donation.invested_amount += donated_amount

        if donation.invested_amount == donation.full_amount:
            donation.fully_invested = True
            donation.close_date = datetime.now()

    if project.invested_amount == project.full_amount:
        project.fully_invested = True
        project.close_date = datetime.now()

    session.add(donation)
    session.add(project)
    await session.commit()
    await session.refresh(donation)
    await session.refresh(project)

    return project, donation
