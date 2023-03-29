from sqlalchemy import Column, Integer, Text


from .base import QRKoTModel


class Donation(QRKoTModel):
    user_id = Column(Integer)
    comment = Column(Text)
