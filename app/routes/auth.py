from fastapi import APIRouter, Depends, HTTPException, status, Request

from fastapi.security.oauth2 import OAuth2PasswordRequestForm


from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud.user import get_user_by_email
from app.core.security import verify_password
from app.core.token import create_access_token
from app.core.oauth import oauth
from app.schemas.user import UserCreate
from app.crud.user import create_user


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login",)
def login(
    db: Session = Depends(get_db),
    user_credentials: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_email(db, user_credentials.username)
    if not user or not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/google")
async def login_google(request: Request):
    redirect_uri = request.url_for('auth_google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/google/callback")
async def auth_google_callback(request: Request, db: Session = Depends(get_db)):

    token = await oauth.google.authorize_access_token(request)
    user_info = token.get('userinfo')
 
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Google authentication",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = get_user_by_email(db, user_info['email'])
    if not user:
        user = create_user(
            db,
            UserCreate(
                email=user_info['email'],
                password="oauth", # Placeholder password, as OAuth users don't have a password
                phone_number=None,
            )
        )
 
    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}