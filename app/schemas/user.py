from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class SignupIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)
    username: Optional[str] = None


class UserOut(BaseModel):
    id: str
    email: EmailStr
    username: Optional[str] = None




