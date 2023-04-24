from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail="Проект с таким именем уже существует!",
        )


async def check_charity_project_exists(
    charity_project_id: int,
    session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(charity_project_id, session)
    if charity_project is None:
        raise HTTPException(status_code=404, detail="Проект не найден!")
    return charity_project


async def check_update_is_possible(
    charity_project_id: int, obj_in, session: AsyncSession
):
    new_full_amount = obj_in.dict()["full_amount"]
    charity_project = await charity_project_crud.get(charity_project_id, session)
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=400, detail="Закрытый проект нельзя редактировать!"
        )

    if (
        new_full_amount
        and charity_project.invested_amount
        and charity_project.invested_amount > new_full_amount
    ):
        raise HTTPException(status_code=422, detail="Нельзя меньше ставить!")


async def check_project_fully_invested(charity_project_id: int, session: AsyncSession):
    charity_project = await charity_project_crud.get(charity_project_id, session)
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=400, detail="Закрытый проект нельзя редактировать!"
        )


async def check_delete_is_possible(charity_project_id: int, session: AsyncSession):
    charity_project = await charity_project_crud.get(charity_project_id, session)

    if charity_project.fully_invested or charity_project.invested_amount:
        raise HTTPException(
            status_code=400,
            detail="В проект были внесены средства, не подлежит удалению!",
        )


async def check_fully_no_less_invested(
    charity_project_id: int, obj_in, session: AsyncSession
):
    new_full_amount = obj_in.dict()["full_amount"]

    charity_project = await charity_project_crud.get(charity_project_id, session)

    if (
        new_full_amount
        and charity_project.invested_amount
        and charity_project.invested_amount > new_full_amount
    ):
        raise HTTPException(status_code=422, detail="Нельзя меньше ставить!")
