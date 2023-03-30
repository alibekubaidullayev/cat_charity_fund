from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectDB,
    CharityProjectCreate,
    CharityProjectUpdate,
)
from app.api.validators import (
    check_charity_project_exists,
    check_name_duplicate,
    check_update_is_possible,
    check_delete_is_possible,
    check_fully_no_less_invested,
)
from app.core.user import current_superuser

router = APIRouter()


@router.get(
    "/", response_model=list[CharityProjectDB], response_model_exclude_none=True
)
async def get_all_charity_projects(session: AsyncSession = Depends(get_async_session)):
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.post(
    "/",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(charity_project.name, session)
    new_charity_project = await charity_project_crud.create(charity_project, session)
    return new_charity_project


@router.delete(
    "/{charity_project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
    charity_project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_charity_project_exists(charity_project_id, session)
    await check_delete_is_possible(charity_project_id, session)
    charity_project = await charity_project_crud.remove(charity_project, session)
    return charity_project


@router.patch(
    "/{charity_project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
    charity_project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_charity_project_exists(charity_project_id, session)
    await check_update_is_possible(charity_project_id, obj_in, session)
    await check_fully_no_less_invested(charity_project_id, obj_in, session)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    return charity_project
