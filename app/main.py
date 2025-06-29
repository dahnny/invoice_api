from fastapi import FastAPI
from app.routes import user, auth, invoice

from starlette.middleware.sessions import SessionMiddleware
from app.core.config import settings 

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.GOOGLE_SECRET_KEY,
)


@app.get("/")
async def root():
    return {"message": "Hello World!"}

app.include_router(user.router, prefix="/api/v1", tags=["users"])
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(invoice.router, prefix="/api/v1", tags=["invoices"])