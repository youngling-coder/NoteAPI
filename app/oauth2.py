from jose import jwt, JWTError
from datetime import datetime, timedelta
from . import schemas, models
from .database import get_db
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = settings.jwt_secret_key
ALGORITHM = settings.jwt_algo
ACCESS_TOKEN_EXPIRE_MINUTES = settings.jwt_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        id = str(payload["user_id"])

        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)

    except JWTError as e:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Couldn't validate credentials!",
                                          headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token=token, credentials_exception=credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
