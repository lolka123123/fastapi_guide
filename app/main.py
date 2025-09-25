from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import engine
from app.routers import item, auth as auth_routes, user as users_routes
from app.db.base import Base


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(auth_routes.router)
app.include_router(users_routes.router)
app.include_router(item.router)
@app.get("/")
async def root():
    return {"status": "ok"}