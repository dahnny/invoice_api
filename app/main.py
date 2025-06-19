from fastapi import FastAPI
from app.routes import user  

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World. This is an invoice service."}

app.include_router(user.router, prefix="/api/v1", tags=["users"])