from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import floor, house, object3d
from backend.models import *
from backend import models 
from .db import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(house.router)
app.include_router(floor.router)
app.include_router(object3d.router)

if __name__ == '__main__':
    models.Base.metadata.create_all(bind=engine)
