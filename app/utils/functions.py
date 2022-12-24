from sqlalchemy.orm import Session

def responseBody(status_code : int, message : str, object = None):
    response =  {
        "status_code" : status_code,
        "message" : message
    }

    if object:
        response.update({"data" : object})

    return response

def dbCommit(db: Session, object):
    db.add(object)
    db.commit()
    db.refresh(object)