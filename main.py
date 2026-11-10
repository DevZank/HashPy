from fastapi import FastAPI
import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

SECRET_KEY = os.getenv("secret_key")
ALGORITHM = os.getenv("ALGORITHM")
ACCES_TOKEN_EXPIRE_MINUTES = 30

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/signin-form")

app = FastAPI()

from auth_routes import auth_router
from order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)

# Para rodar: uvicorn main:app --reload