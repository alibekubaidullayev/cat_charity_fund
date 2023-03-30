from pydantic import Extra
from sqlalchemy import Column, String, Text

from app.core.db import Base
from .base import QRKoTModel


class CharityProject(Base, QRKoTModel):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)

    class Config:
        extra = Extra.allow