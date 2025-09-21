from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.core.security import verify_password, hash_password


async def get_by_email(db: AsyncSession, email: str) -> User | None:
    return await db.scalar(select(User).where(User.email == email))


async def create(db: AsyncSession, email: str, password: str, username: str | None) -> User:
    user = User(email=email, username=username, password_hash=await hash_password(password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def authenticate(db: AsyncSession, email: str, password: str) -> User | None:
    user = await get_by_email(db, email)
    if not user or not user.is_active:
        return None
    if not await verify_password(password, user.password_hash):
        return None
    return user