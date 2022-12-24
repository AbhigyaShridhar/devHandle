from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean

from app.server.database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    content = Column(String, index=False, nullable=False, default="")
    code = Column(String, index=False, nullable=True)
    author = Column(Integer, ForeignKey("users.id"))

class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    content = Column(String, index=False, nullable=False, default="")
    post = Column(Integer, ForeignKey("posts.id"))
    author = Column(Integer, ForeignKey("users.id"))
    accepted = Column(Boolean, nullable=False, default=False)

class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type = Column(String, index=False, nullable=False, default="up")
    post = Column(Integer, ForeignKey("posts.id"))
    author = Column(Integer, ForeignKey("users.id"))

class Diamond(Base):
    __tablename__ = "diamonds"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    answer = Column(Integer, ForeignKey("answers.id"))
