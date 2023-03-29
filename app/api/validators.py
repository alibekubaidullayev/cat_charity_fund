from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject, User


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    room_id = await charity_project_crud.get_project_id_by_name(project_name, session)
    if room_id is not None:
        raise HTTPException(
            status_code=422,
            detail="Переговорка с таким именем уже существует!",
        )


async def check_charity_project_exists(
    charity_project_id: int,
    session: AsyncSession,
) -> CharityProject:
    meeting_room = await charity_project_crud.get(charity_project_id, session)
    if meeting_room is None:
        raise HTTPException(status_code=404, detail="Проект не найден!")
    return meeting_room
