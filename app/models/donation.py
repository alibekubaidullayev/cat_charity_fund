from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base
from app.models.user import User

from .base import ProjectDonationMixin


class Donation(Base, ProjectDonationMixin):
    user_id = Column(Integer, ForeignKey(User.id))
    comment = Column(Text)
