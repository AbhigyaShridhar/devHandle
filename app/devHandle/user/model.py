from sqlalchemy import Column, Integer, String

from app.server.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, index=True, nullable=False, default="johnDoe")
    email = Column(String, index=True, nullable=False, default="johndoe@gmail.com")
    reputation = Column(Integer, index=False, nullable=False, default=0)
    diamonds = Column(Integer, index=False, nullable=False, default=0)