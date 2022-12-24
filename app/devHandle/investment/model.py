from sqlalchemy import Column, Integer, Float
from sqlalchemy.sql.schema import ForeignKey

from app.server.database import Base

class Investment(Base):
    __tablename__ = "investments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    investor = Column(Integer, ForeignKey("users.id"))
    user = Column(Integer, ForeignKey("users.id"))
    startingReputation = Column(Integer, index=False, nullable=False, default=0)
    currentReputation = Column(Integer, index=False, nullable=False, default=0)
    amount = Column(Float, nullable=False, default=0.5)