from fastapi import FastAPI

from backend.routes import floor, house, object3d

app = FastAPI()


app.include_router(house.router)
app.include_router(floor.router)
app.include_router(object3d.router)


 
