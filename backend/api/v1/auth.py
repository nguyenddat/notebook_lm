from typing import *

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from db import get_db
from service import UserService
from schema import UserRegister
from utils import create_access_token, create_refresh_token


router = APIRouter()


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Đăng nhập và lấy token"""
    user = UserService.authenticate(form_data, db)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/register")
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Đăng ký người dùng mới"""
    try:
        user = UserService.create(user_data, db)
        access_token = create_access_token(subject=user.id)
        refresh_token = create_refresh_token(subject=user.id)

        db.commit()
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    