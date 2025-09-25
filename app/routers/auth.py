from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import SignupIn, UserOut
from app.schemas.auth import TokenPair, RefreshIn
from app.crud import user as user_crud
from app.crud import refresh_token as rt_crud
from app.core.security import create_access_token, create_refresh_token
from app.db.session import get_session, get_current_user
from app.core.security import decode_token


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=UserOut, status_code=201)
async def signup(data: SignupIn, db: AsyncSession = Depends(get_session)):
    if await user_crud.get_by_email(db, data.email):
        raise HTTPException(status_code=400, detail="User already exists")
    u = await user_crud.create(db, data.email, data.password, data.username)
    return UserOut(id=u.id, email=u.email, username=u.username)


@router.post("/login", response_model=TokenPair)
async def login(form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    u = await user_crud.authenticate(db, form.username, form.password)
    if not u:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access = create_access_token(u.email)
    refresh, jti, exp = create_refresh_token(u.email)
    await rt_crud.store(db, u, jti, exp)
    return TokenPair(access_token=access, refresh_token=refresh)


@router.post("/refresh", response_model=TokenPair)
async def refresh(body: RefreshIn, db: AsyncSession = Depends(get_session)):
    payload = decode_token(body.refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Refresh token required")
    jti, email = payload.get("jti"), payload.get("sub")
    rec = await rt_crud.ensure_valid(db, jti)
    rec.revoked = True
    u = await user_crud.get_by_email(db, email)
    if not u:
        await db.commit()
        raise HTTPException(status_code=401, detail="User not found")
    new_access = create_access_token(email)
    new_refresh, new_jti, new_exp = create_refresh_token(email)
    await rt_crud.store(db, u, new_jti, new_exp)
    await db.commit()
    return TokenPair(access_token=new_access, refresh_token=new_refresh)

@router.post("/logout")
async def logout(body: RefreshIn, db: AsyncSession = Depends(get_session)):
    payload = decode_token(body.refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Refresh token required")
    ok = await rt_crud.revoke_by_jti(db, payload.get("jti"))
    if not ok:
        raise HTTPException(status_code=400, detail="Token not found")
    return {"detail": "Logged out (token revoked)"}


@router.post("/logout_all")
async def logout_all(current_user=Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    n = await rt_crud.revoke_all_for_user(db, current_user.id)
    return {"detail": f"Revoked {n} refresh tokens"}


