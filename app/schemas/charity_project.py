from typing import Optional
from datetime import datetime, timedelta

from pydantic import BaseModel, Field, root_validator, PositiveInt, validator


FROM_TIME = (datetime.now() + timedelta(minutes=10)).isoformat(timespec="minutes")
TO_TIME = (datetime.now() + timedelta(hours=1)).isoformat(timespec="minutes")


class CharityProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str
    invested_amount: int = Field(default=0)
    fully_invested: bool = Field(default=False)


class CharityProjectCreate(CharityProjectBase):
    full_amount: PositiveInt
    create_date: datetime = datetime.now()
    close_date: Optional[datetime] = None

    @validator("description")
    def non_empty_description(cls, value):
        if not value:
            raise ValueError("Описание не может быть пустым")
        return value


class CharityProjectDB(CharityProjectCreate):
    id: int

    class Config:
        orm_mode = True


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    @root_validator(skip_on_failure=True)
    def check_full_amount_no_less_than_invested(cls, values):
        if (
            values["full_amount"] is not None
            and values["full_amount"] < values["invested_amount"]
        ):
            raise ValueError("Полная сумма не может быть меньше уже имеющейся!")
        return values
