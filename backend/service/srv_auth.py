from typing import Optional

from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer


from config import config
from model import User
from schema import UserLogin, UserRegister, TokenData
from utils import verify_password, get_password_hash
from db import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

class UserService(object):
    @staticmethod
    def authenticate(user: OAuth2PasswordBearer, db: Session) -> Optional[User]:
        """
        Check username and password is correct.
        Return object User if correct, else return None
        """
        existed_user = db.query(User).filter_by(username=user.username).first()
        if (existed_user) and (verify_password(user.password, existed_user.password)):
            return existed_user

        return None

    @staticmethod
    def create(data: UserRegister, db: Session) -> User:
        exist_user = db.query(User).filter(User.username == data.username).first()
        if exist_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        register_user = User(
            username=data.username,
            password=get_password_hash(data.password),
            role=data.role,
        )
        db.add(register_user)
        db.flush()
        return register_user


    @staticmethod
    def get_current_user(
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme), 
    ) -> User:
        """Lấy thông tin người dùng hiện tại từ token"""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, config.secret_key, algorithms=[config.security_algorithm])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception
            token_data = TokenData(user_id=user_id)
        except JWTError as err:
            raise credentials_exception

        user = db.query(User).filter(User.id == token_data.user_id).first()
        if user is None:
            raise credentials_exception
        
        return user

    @staticmethod
    def admin_required(current_user: User = Depends(get_current_user)) -> User:
        """Kiểm tra người dùng hiện tại có phải là admin không"""
        if not current_user.role == "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="The user doesn't have enough privileges",
            )
        return current_user
    

    @staticmethod
    def login_required(current_user: User = Depends(get_current_user)) -> User:
        """Kiểm tra người dùng hiện tại đã đăng nhập không"""
        # current_user lúc này đã được FastAPI inject từ get_current_user
        if current_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized",
            )
        return current_user