from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import or_, and_

from .model import Investment
from ..user.model import User
from .schema import investmentSchema
from ...utils.functions import dbCommit, responseBody

def getInvestments(db: Session, userId: int):
    try:
        investments = db.query(Investment).filter(Investment.investor==userId).all()
        for investment in investments:
            investment = investment.__dict__
            investment["user"] = db.query(User).filter(User.id==investment["user"]).first().__dict__
        response = {
            "investments": investments
        }
        return responseBody(201, "User investments", response)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


def getInvestors(db: Session, userId: int):
    try:
        investors = db.query(Investment).filter(Investment.user==userId).all()
        for investor in investors:
            investor = investor.__dict__
            investor["user"] = db.query(User).filter(User.id==investor["investor"]).first().__dict__
        response = {
            "investors": investors
        }
        return responseBody(201, "User investors", response)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


def getInvestmentDetails(investmentId: int, db: Session, userId: int):
    try:
        investment = db.query(Investment).filter(Investment.id==investmentId).first()
        if investment.id == userId:
            response = {
                investment
            }
            return responseBody(201, "investment details", response)
        else:
            return responseBody(300, "invalid operation")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


def invest(db: Session, data: investmentSchema, userId: int):
    try:
        if userId == data.user:
            return responseBody(300, "Can't invest in yourself")
        iUser = db.query(User).filter(User.id==data.user)
        investment = Investment(
            amount = data.amount,
            user = data.user,
            investor = userId,
            startingReputation = iUser.first().reputation,
            currentReputation = iUser.first().reputation
        )
        dbCommit(db, investment)
        iUser.update({'reputation': iUser.first().reputation})
        db.commit()
        db.refresh(iUser.first())

        return responseBody(201, "new investment made", investment.__dict__)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


def checkout(db: Session, investmentId: int, userId: int):
    try:
        investment = db.query(Investment).filter(Investment.id==investmentId).first()
        db.delete(investment)
        db.commit()
        return responseBody(200, "checked out successfully")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
