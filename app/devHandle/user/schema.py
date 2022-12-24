from pydantic import BaseModel, EmailStr, Field

class signupSchema(BaseModel):
    username: str = Field(...,example='johnDoe')
    email: EmailStr = Field(...,example='johndoe@gmail.com')

class loginSchema(BaseModel):
    username: str = Field(...,example='johnDoe')