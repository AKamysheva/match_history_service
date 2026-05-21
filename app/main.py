from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers.admin import router as admin_router
from app.routers.players import router as player_router
from app.dependencies import riot_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await riot_client.close()


app = FastAPI(lifespan=lifespan)


app.include_router(admin_router)
app.include_router(player_router)


@app.get("/")
async def root():
    return {"status": "ok"}
