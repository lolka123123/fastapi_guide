from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from fastapi import HTTPException

from app.models.user import RefreshToken


async def store(db: AsyncSession, user, jti: str, expires_at: datetime) -> None:
    db.add(RefreshToken(jti=jti, user=user, expires_at=expires_at, created_at=datetime.utcnow()))
    await db.commit()


async def revoke_by_jti(db: AsyncSession, jti: str) -> bool:
    rec = await db.scalar(select(RefreshToken).where(RefreshToken.jti == jti))
    if not rec:
        return False
    rec.revoked = True
    await db.commit()
    return True


async def revoke_all_for_user(db: AsyncSession, user_id: int) -> int:
    recs = (await db.scalars(select(RefreshToken).where(RefreshToken.user_id == user_id, RefreshToken.revoked == False))).all()
    for r in recs:
        r.revoked = True
    n = len(recs)
    if n:
        await db.commit()
    return n


async def ensure_valid(db: AsyncSession, jti: str) -> RefreshToken:
    rec = await db.scalar(select(RefreshToken).where(RefreshToken.jti == jti))
    if not rec or rec.revoked:
        raise HTTPException(status_code=401, detail="Refresh token revoked or unknown")
    if rec.expires_at <= datetime.utcnow().astimezone(rec.expires_at.tzinfo):
        rec.revoked = True
        await db.commit()
        raise HTTPException(status_code=401, detail="Refresh token expired")
    return rec