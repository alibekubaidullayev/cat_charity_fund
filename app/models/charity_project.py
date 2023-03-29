from sqlalchemy import Column, String, Text

from .base import QRKoTModel


class CharityProject(QRKoTModel):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
