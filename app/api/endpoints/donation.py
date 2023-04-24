from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB, DonationRead
from app.services import invest_donation

router = APIRouter()


@router.get("/", response_model=list[DonationDB], response_model_exclude_none=True)
async def get_all_donations(session: AsyncSession = Depends(get_async_session)):
    all_projects = await donation_crud.get_multi(session)
    return all_projects


@router.post(
    "/",
    response_model=DonationRead,
    response_model_exclude_none=True,
)
async def create_new_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    new_donation = await donation_crud.create(donation, session, user)
    new_donation = await invest_donation(new_donation, session)
    return new_donation


@router.get("/my", response_model=list[DonationRead], response_model_exclude_none=True)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    all_donations = await donation_crud.get_multi(session, user)
    return all_donations
