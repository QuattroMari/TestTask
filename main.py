from fastapi import FastAPI
from contextlib import asynccontextmanager
from services.db import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
    

app = FastAPI(title="Аггрегатор продаж", lifespan=lifespan)
