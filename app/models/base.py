from sqlalchemy import Boolean, Column, DateTime, Integer, func


class QRKoTModel:
    full_amount = Column(Integer)
    invested_amount = Column(Integer)
    fully_invested = Column(Boolean)
    create_date = Column(DateTime, server_default=func.now())
    close_date = Column(DateTime)
