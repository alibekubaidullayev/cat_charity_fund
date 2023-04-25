from sqlalchemy import Column, String, Text

from app.core.db import Base

from .base import ProjectDonationMixin


class CharityProject(Base, ProjectDonationMixin):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
