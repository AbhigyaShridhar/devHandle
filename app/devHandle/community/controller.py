from app.server.database import get_db
from app.utils.jwtHandler import hasAccess
from .helper import getPostDetails, createPost, upvotePost, downvotePost, giveDiamond, acceptAnswer, createAnswer
from .schema import postSchema, answerSchema
from fastapi import  Depends, APIRouter
from sqlalchemy.orm import Session

communityRouter = APIRouter()

@communityRouter.get('/detail')
def call(postId: int, db: Session = Depends(get_db)):
    return getPostDetails(db, postId)

@communityRouter.post('/ask')
def call(data: postSchema, key = Depends(hasAccess), db: Session = Depends(get_db)):
    return createPost(db, data, key['id'])

@communityRouter.post('/answer')
def call(data: answerSchema, key = Depends(hasAccess), db: Session = Depends(get_db)):
    return createAnswer(db, data, key['id'])

@communityRouter.put('/accept')
def call(answerId: int, key = Depends(hasAccess), db: Session = Depends(get_db)):
    return acceptAnswer(db, answerId, key['id'])

@communityRouter.put('/upvote')
def call(postId: int, key = Depends(hasAccess), db: Session = Depends(get_db)):
    return upvotePost(db, postId ,key['id'])

@communityRouter.put('/downvote')
def call(postId: int, key = Depends(hasAccess), db: Session = Depends(get_db)):
    return downvotePost(db, postId, key['id'])

@communityRouter.put('/diamond')
def call(answerId: int, key = Depends(hasAccess), db: Session = Depends(get_db)):
    return giveDiamond(db, answerId, key['id'])


