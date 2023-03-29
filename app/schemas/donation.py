from datetime import datetime, timedelta

from pydantic import BaseModel, Field, PositiveInt


FROM_TIME = (datetime.now() + timedelta(minutes=10)).isoformat(timespec="minutes")
TO_TIME = (datetime.now() + timedelta(hours=1)).isoformat(timespec="minutes")


class DonationBase(BaseModel):
    invested_amount: PositiveInt = 0
    fully_invested: bool = False
    create_date: datetime = Field(..., example=FROM_TIME)
    close_date: datetime = Field(..., example=TO_TIME)


class DonationCreate(DonationBase):
    comment: str
    full_amount: PositiveInt


class DonationDB(DonationCreate):
    id: int
    user_id: int

    class Config:
        orm_mode = True
