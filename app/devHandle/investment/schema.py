from pydantic import BaseModel, Field

class investmentSchema(BaseModel):
    amount: float = Field(...,example=0.5)
    user: int = Field(...,example=1)
