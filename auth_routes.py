from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import get_session
from main import bcrypt_context
from schemas import UserSchema
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def auth():
    """
    Essa é a rota padrão de autenticação da API!
    """
    return {"Message": "Access granted!", "Authenticated": False}

@auth_router.post("/createUser")
async def create_account(user_schema: UserSchema, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.email==user_schema.email).first()

    if user:
        raise HTTPException(status_code=400, detail="User already exists!")
    else:
        encrypted_password = bcrypt_context.hash(user_schema.password)
        new_user = User(user_schema.name, user_schema.password, encrypted_password, user_schema.active, user_schema.admin)
        session.add(new_user)
        session.commit()
        return {"Message": f"User created! {user_schema.email}"}