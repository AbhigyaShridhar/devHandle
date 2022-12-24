from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import or_, and_

from .model import User
from ..community.model import Post, Answer, Diamond, Vote
from .schema import loginSchema, signupSchema
from ...utils.functions import dbCommit, responseBody
from ...utils.jwtHandler import signJWT

def getUserData(db: Session, db_user: User):
    response = db_user.__dict__
    posts = db.query(Post).filter(Post.author==db_user.id).all()
    answers = db.query(Answer).filter(Answer.author==db_user.id).all()
    for answer in answers:
        answer = answer.__dict__
        answer["diamonds"] = db.query(Diamond).filter(Diamond.answer==answer["id"]).count()
    for post in posts:
        post = post.__dict__
        post['votes'] = db.query(Vote).filter(and_(Vote.type=="up", Vote.post==post["id"])).count() - db.query(Vote).filter(and_(Vote.type=="down", Vote.post==post["id"])).count()
    response["posts"] = posts
    response["answers"] = answers
    return response

def getUserDetails(db: Session, id: str):
    try:
        db_user = db.query(User).filter(User.id==id).first()
        if not db_user: return responseBody(401, "Invalid Token")
        response = getUserData(db, db_user)
        return responseBody(200,"user details",response)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

def checkUserExist(db: Session, username: str, email: Optional[str] = None):
    return db.query(User).filter(or_(User.username==username,User.email==email)).first()

def signup(db: Session, data: signupSchema):
    try:
        if checkUserExist(db,data.username,data.email) is not None:
            return responseBody(409, "username or email is already taken!")

        db_user = User(email=data.email, username=data.username)
        dbCommit(db, db_user)

        db.commit()

        userData = getUserData(db, db_user)
        response = {
            "user": userData,
            "Token": signJWT(db_user)
        }
        return responseBody(201,"User created successfully", response)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

def login(db: Session, data: loginSchema):
    try:
        db_user = checkUserExist(db, data.username)
        if not db_user:
            return responseBody(404,"User doesn't exist!")

        if db_user:
            userData = getUserData(db, db_user)
            response = {
                "user": userData,
                "Token": signJWT(db_user)
            }
            return responseBody(200,"User login success",response)
        else:
            return responseBody(404,"User not found!")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail=str(e))
