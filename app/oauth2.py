import imp
from jose import JWTError, jwt
from datetime import datetime, timedelta

from app import database, schemas

from . import schemas, models
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#SECRET_KEY
#Algorithm
#expiration time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_enocde = data.copy()
    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_enocde.update({"exp":expire})

    encoded_jwt = jwt.encode(to_enocde,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, crednetials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])

        id: str = payload.get("user_id")
        if id is None:
            raise crednetials_exception
        
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise crednetials_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db:Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials",headers={"WWW-Authenticate":"Bearer"})

    token = verify_access_token(token,credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
