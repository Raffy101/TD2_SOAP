from fastapi import FastAPI,Depends,HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base,sessionmaker, relationship
from passlib.context import CryptContext
import urllib.parse

engine = create_engine('sqlite:///./DataBase/baseDonneeClients.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#openssl rand -hex 32
SECRET_KEY = "5c3b061802c10bf71b8f52d262274904ebd0802a523f89c5c65c6428ab47dc9b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

# Déclarer la classe de modèle (représente une table dans la base de données)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    username = Column(String(50))
    password = Column(String(50))
    email = Column(String(50))
    stats = relationship('StatistiquesClient', back_populates='user')
    transactions = relationship('Transactions', back_populates='user')

class StatistiquesClient(Base):
    __tablename__ = 'statistiquesClient'
    id = Column(Integer, primary_key=True, index=True)
    id_Client = Column(Integer, ForeignKey("users.id"))
    total_credit = Column(Integer)
    nb_faillites = Column(Integer)
    nb_retards = Column(Integer)
    user = relationship('User', back_populates='stats')

class Transactions(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, index=True)
    id_Client = Column(Integer, ForeignKey('users.id'))
    montant = Column(Integer)
    date_payement = Column(String(15))
    user = relationship('User', back_populates='transactions')

def is_allowed_file(filename): 
  return filename.lower().endswith(".txt")
    
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

app = FastAPI()
router = APIRouter()

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = session.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

#Creation token simple test
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#Creation du token jwt
"""def create_access_token(data: dict, expires_delta: timedelta | None = None):
    header = {"alg": ALGORITHM, "typ": "JWT"}
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"iat": datetime.utcnow(), "exp": expire})
    # Encode the header
    encoded_header = jwt.encode(header, key=None, algorithm=ALGORITHM)
    # Encode the payload
    encoded_payload = jwt.encode(to_encode, key=None, algorithm=ALGORITHM)
    # Concatenate header and payload with a period
    encoded_token = encoded_header.decode('utf-8') + "." + encoded_payload.decode('utf-8')
    # Calculate the signature
    signature = jwt.encode(encoded_token.encode('utf-8'), key=SECRET_KEY, algorithm=ALGORITHM)
    # Concatenate token and signature
    encoded_jwt = encoded_token + "." + signature.decode('utf-8')

    return encoded_jwt"""

def authenticate_user(username: str, password: str):
    client_trouve = session.query(User).filter(User.username == username).first()
    if not client_trouve:
        return False
    if not verify_password(password, client_trouve.password):
        return False
    return client_trouve
