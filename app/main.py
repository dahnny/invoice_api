from fastapi import FastAPI
from app.routes import user 
from app.routes import auth 

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World. This is an invoice service."}

app.include_router(user.router, prefix="/api/v1", tags=["users"])
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])