from fastapi import FastAPI

from backend.routes import items

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(items.router)





 
