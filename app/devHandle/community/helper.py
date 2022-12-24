from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import and_

from .model import Post, Answer, Vote, Diamond
from .schema import postSchema, answerSchema
from ...utils.functions import dbCommit, responseBody

def getPostDetails(db: Session, postId: int):
    try:
        post = db.query(Post).filter(Post.id==postId).first()
        if not post: return responseBody(401, "Invalid Token")
        post = post.__dict__
        answers = db.query(Answer).filter(Answer.post==postId).all()
        for answer in answers:
            answer = answer.__dict__
            answer["diamonds"] = db.query(Diamond).filter(Diamond.answer==answer["id"]).count()
        post["votes"] = db.query(Vote).filter(and_(Vote.type=="up", Vote.post==postId)).count() - db.query(Vote).filter(and_(Vote.type=="down", Vote.post==postId)).count()
        post["replies"] = answers
        return responseBody(200,"user details",post)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Something went wrong")


def createPost(db: Session, data: postSchema, userId: int):
    try:
        post = Post(
            content = data.content,
            code = data.code,
            author = userId
        )
        dbCommit(db, post)
        return responseBody(201,"Post created successfully", post.__dict__)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Something went wrong!")


def upvotePost(db: Session, postId: int, userId: int):
    try:
        sameVote = db.query(Vote).filter(and_(Vote.type=='up', Vote.post==postId, Vote.author==userId)).first()
        vote = db.query(Vote).filter(and_(Vote.type=='down', Vote.post==postId, Vote.author==userId)).first()
        if vote:
            db.delete(vote)
            db.commit()
        elif sameVote:
            return responseBody(300, "Already voted")
        else:
            vote = Vote(
                type = "up",
                author = userId,
                post = postId
            )
            dbCommit(db, vote)
        return responseBody(201, "post upvoted successfully")

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Something went wrong!")


def downvotePost(db: Session, postId: int, userId: int):
    try:
        sameVote = db.query(Vote).filter(and_(Vote.type=='down', Vote.post==postId, Vote.author==userId)).first()
        vote = db.query(Vote).filter(and_(Vote.type=='up', Vote.post==postId, Vote.author==userId)).first()
        if vote:
            db.delete(vote)
            db.commit()
        elif sameVote:
            return responseBody(300, "already downvoted")
        else:
            vote = Vote(
                type = "down",
                author = userId,
                post = postId
            )
            dbCommit(db, vote)

        return responseBody(201,"Post downvoted successfully")

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Something went wrong!")


def giveDiamond(db: Session, answerId: int, userId: int):
    try:
        diamond = Diamond(
            answer = answerId
        )
        dbCommit(db, diamond)

        return responseBody(201,"Diamond donated successfully")

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Something went wrong!")


def acceptAnswer(db: Session, answerId: int, userId: int):
    try:
        answer = db.query(Answer).filter(Answer.id==answerId)
        question = db.query(Post).filter(Post.id==answer.first().post).first()
        if question.author == userId:
            answer.update({'accepted': True})
            db.commit()
            db.refresh(answer.first())
            response = {
                'answer': answer.first()
            }
            return responseBody(201,"Answer accepted as solution", response)
        else:
            return responseBody(300, "invalid operation")

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Something went wrong!")


def createAnswer(db: Session, data: answerSchema, userId: int):
    try:
        answer = Answer(
            content = data.content,
            author = userId,
            post = data.postId
        )
        dbCommit(db, answer)

        response = {
            "newAnswer": answer.__dict__
        }
        return responseBody(201,"Answer created successfully", response)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Something went wrong!")

