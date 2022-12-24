from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from enum import Enum
from fastapi.params import Param
from sqlalchemy.sql.schema import Column

class postSchema(BaseModel):
    content: str = Field(...,example='some question about something?')
    code: str = Field(...,example='int main()')

class answerSchema(BaseModel):
    content: str = Field(...,example='some markdown content')
    postId: int = Field(...,example=1)