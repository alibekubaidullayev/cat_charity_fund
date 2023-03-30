from typing import Optional
from datetime import datetime, timedelta

from pydantic import BaseModel, PositiveInt, NonNegativeInt, root_validator


FROM_TIME = (datetime.now() + timedelta(minutes=10)).isoformat(timespec="minutes")
TO_TIME = (datetime.now() + timedelta(hours=1)).isoformat(timespec="minutes")


class DonationCreate(BaseModel):
    invested_amount: NonNegativeInt = 0
    fully_invested: bool = False
    create_date: Optional[datetime] = datetime.now()
    comment: str
    full_amount: PositiveInt


class DonationDB(DonationCreate):
    id: int
    user_id: int
    close_date: Optional[datetime] = None

    class Config:
        orm_mode = True


class DonationRead(BaseModel):
    comment: str
    full_amount: PositiveInt
    create_date: Optional[datetime] = datetime.now()
    id: int

    @root_validator
    def defaults(cls, values):
        if values.get("invested_amount") is None:
            values["invested_amount"] = 0
        if values.get("fully_invested") is None:
            values["fully_invested"] = False
        return values

    class Config:
        orm_mode = True
