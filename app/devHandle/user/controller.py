from fastapi import  Depends, APIRouter
from sqlalchemy.orm import Session
from app.server.database import get_db
from app.utils.jwtHandler import hasAccess
from .helper import getUserDetails, signup, login
from .schema import signupSchema, loginSchema

userRouter = APIRouter()
authRouter = APIRouter()

@userRouter.get('/detail')
def call(key = Depends(hasAccess), db: Session = Depends(get_db)):
    return getUserDetails(db, key['id'])

@authRouter.post('/signup')
def call(data: signupSchema, db: Session = Depends(get_db)):
    return signup(db, data)

@authRouter.post('/login')
def call(data: loginSchema, db: Session = Depends(get_db)):
    return login(db, data)