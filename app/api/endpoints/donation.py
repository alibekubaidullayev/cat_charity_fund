from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.donation import donation_crud
from app.schemas.donation import (
    DonationDB,
    DonationCreate,
)
from app.core.user import current_superuser

router = APIRouter()


@router.get("/", response_model=list[DonationDB], response_model_exclude_none=True)
async def get_all_donations(session: AsyncSession = Depends(get_async_session)):
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.get("/my", response_model=list[DonationDB], response_model_exclude_none=True)
async def get_all_charity_projects(session: AsyncSession = Depends(get_async_session)):
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.post(
    "/",
    response_model=DonationDB,
    response_model_exclude_none=True,
)
async def create_new_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
):
    new_donation = await charity_project_crud.create(donation, session)
    return new_donation
