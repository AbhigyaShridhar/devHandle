from fastapi import  Depends, APIRouter
from sqlalchemy.orm import Session
from app.server.database import get_db
from app.utils.jwtHandler import hasAccess
from .helper import getInvestments, getInvestors, getInvestmentDetails, invest, checkout
from .schema import investmentSchema

investorRouter = APIRouter()

@investorRouter.get('/investments')
def call(key = Depends(hasAccess), db: Session = Depends(get_db)):
    return getInvestments(db, key['id'])

@investorRouter.get('/investors')
def call(key = Depends(hasAccess), db: Session = Depends(get_db)):
    return getInvestors(db, key['id'])

@investorRouter.get('/investmentDetails')
def call(id: int, key = Depends(hasAccess), db: Session = Depends(get_db)):
    return getInvestmentDetails(id, db, key['id'])

@investorRouter.post('/invest')
def call(data: investmentSchema, key = Depends(hasAccess), db: Session = Depends(get_db)):
    return invest(db, data, key['id'])

@investorRouter.post('/checkout')
def call(investmentId: int, key = Depends(hasAccess), db: Session = Depends(get_db)):
    return checkout(db, investmentId, key['id'])
