from fastapi import FastAPI

from .routers import hello

app = FastAPI(title="APIs FastAPI", version="0.1.0")

app.include_router(hello.router)
