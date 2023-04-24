from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, root_validator, validator


class CharityProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str
    invested_amount: Optional[int]
    fully_invested: Optional[bool]
    create_date: Optional[datetime]
    close_date: Optional[datetime]


class CharityProjectCreate(CharityProjectBase):
    full_amount: PositiveInt

    @validator("description")
    def non_empty_description(cls, value):
        if not value:
            raise ValueError("Описание не может быть пустым")
        return value


class CharityProjectDB(CharityProjectCreate):
    id: int

    class Config:
        orm_mode = True


class CharityProjectUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    @root_validator
    def non_empty(cls, values):
        for key, value in values.items():
            if value == "":
                raise ValueError(f"{key} не  может быть пустым!!")
        return values

    class Config:
        extra = "forbid"
