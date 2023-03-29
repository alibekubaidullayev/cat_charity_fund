from typing import Optional
from datetime import datetime, timedelta

from pydantic import BaseModel, Field, root_validator, PositiveInt


FROM_TIME = (datetime.now() + timedelta(minutes=10)).isoformat(timespec="minutes")
TO_TIME = (datetime.now() + timedelta(hours=1)).isoformat(timespec="minutes")


class CharityProjectBase(BaseModel):
    invested_amount: PositiveInt = 0
    fully_invested: bool = False
    create_date: datetime = Field(..., example=FROM_TIME)
    close_date: datetime = Field(..., example=TO_TIME)


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=1, max_length=100)
    description: str
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectCreate):
    name: Optional[str] = Field(..., min_length=1, max_length=100)
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    @root_validator(skip_on_failure=True)
    def check_full_amount_no_less_than_invested(cls, values):
        if values["full_amount"] < values["invested_amount"]:
            raise ValueError("Полная сумма не может быть меньше уже имеющейся!")
        return values


class CharityProjectDB(CharityProjectCreate):
    id: int

    class Config:
        orm_mode = True
