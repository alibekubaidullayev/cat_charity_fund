from fastapi import HTTPException
from typing import Optional
from datetime import datetime, timedelta

from pydantic import BaseModel, Field, root_validator, PositiveInt, validator


FROM_TIME = (datetime.now() + timedelta(minutes=10)).isoformat(timespec="minutes")
TO_TIME = (datetime.now() + timedelta(hours=1)).isoformat(timespec="minutes")


class CharityProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str
    invested_amount: Optional[int]
    fully_invested: Optional[bool]
    create_date: Optional[datetime] = datetime.now()
    close_date: Optional[datetime] = None

    @root_validator
    def defaults(cls, values):
        if values.get("invested_amount") is None:
            values["invested_amount"] = 0
        if values.get("fully_invested") is None:
            values["fully_invested"] = False
        return values


class CharityProjectCreate(CharityProjectBase):
    full_amount: PositiveInt

    @validator("description")
    def non_empty_description(cls, value):
        if not value:
            raise HTTPException(
                status_code=422,
                detail="Описание не может быть пустым",
            )
        return value


class CharityProjectDB(CharityProjectCreate):
    id: int

    class Config:
        orm_mode = True


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str]
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    @root_validator()
    def non_empty(cls, values):
        for key in values:
            if key == "":
                raise ValueError(f"{key} не  может быть пустым!")
