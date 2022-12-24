import time
import jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..devHandle.user.model import User

JWT_SECRET = 'bfef766459037880e6740c1a354cf24e'
JWT_ALGORITHM = 'HS256'

security = HTTPBearer()

async def hasAccess(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = decodeJWT(token)
        if payload: return payload
        else: raise HTTPException(
            status_code=401,
            detail='Invalid token')
    except:
        raise HTTPException(
            status_code=401,
            detail='Invalid token')

def signJWT(user: User):
    payload={
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "expiry": time.time() + 86400
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def decodeJWT(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decode_token #if decode_token['expiry'] >= time.time() else None
    except:
        return {}