from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.schemas import item as schemas
from app.models import item as model

router = APIRouter(prefix="/items", tags=["items"])

db_dependence = Depends(get_session)


@router.get("/", status_code=status.HTTP_200_OK)
async def list_items(db: AsyncSession = db_dependence):
    result = await db.execute(select(model.Item))
    return result.scalars().all()

@router.get('/{item_id}', status_code=status.HTTP_302_FOUND)
async def get_item(item_id: int, db: AsyncSession = db_dependence):
    res = await db.execute(select(model.Item).where(model.Item.id == item_id))
    item = res.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_item(payload: schemas.ItemBase, db: AsyncSession = db_dependence):
    item = model.Item(title=payload.title, price=payload.price)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


