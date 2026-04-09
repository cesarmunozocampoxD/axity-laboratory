from contextlib import asynccontextmanager

from fastapi import FastAPI

from .db.init_db import create_tables
from .routers import auth, hello, orders


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(title="APIs FastAPI", version="0.1.0", lifespan=lifespan)

app.include_router(hello.router)
app.include_router(auth.router)
app.include_router(orders.router)
