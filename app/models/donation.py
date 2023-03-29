from sqlalchemy import Column, Integer, Text

from app.core.db import Base
from .base import QRKoTModel


class Donation(Base, QRKoTModel):
    user_id = Column(Integer)
    comment = Column(Text)
