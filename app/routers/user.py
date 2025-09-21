from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserOut
from app.database import get_current_user


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserOut)
async def read_me(current_user=Depends(get_current_user)):
    return UserOut(id=current_user.id, email=current_user.email, username=current_user.username)

