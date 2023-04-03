from typing import Optional
from datetime import datetime, timedelta

from pydantic import BaseModel, PositiveInt, NonNegativeInt, root_validator


FROM_TIME = (datetime.now() + timedelta(minutes=10)).isoformat(timespec="minutes")
TO_TIME = (datetime.now() + timedelta(hours=1)).isoformat(timespec="minutes")


class DonationCreate(BaseModel):
    invested_amount: Optional[NonNegativeInt]
    fully_invested: Optional[bool]
    create_date: Optional[datetime]
    comment: Optional[str]
    full_amount: PositiveInt

    @root_validator
    def defaults(cls, values):
        if values.get("invested_amount") is None:
            values["invested_amount"] = 0
        if values.get("fully_invested") is None:
            values["fully_invested"] = False
        return values


class DonationDB(DonationCreate):
    id: int
    user_id: int
    close_date: Optional[datetime] = None

    class Config:
        orm_mode = True


class DonationRead(BaseModel):
    comment: Optional[str]
    full_amount: PositiveInt
    create_date: Optional[datetime]
    id: int

    class Config:
        orm_mode = True