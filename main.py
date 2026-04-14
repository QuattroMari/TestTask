from fastapi import FastAPI
from contextlib import asynccontextmanager

from services.db import engine, Base
from routers import sales

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
    

app = FastAPI(title="Аггрегатор продаж", lifespan=lifespan)

app.include_router(sales.router)
