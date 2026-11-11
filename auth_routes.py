from fastapi import APIRouter
from models import User, db
from sqlalchemy.orm import sessionmaker

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def auth():
    """
    Essa é a rota padrão de autenticação da API!
    """
    return {"Message": "Access granted!", "Authenticated": False}

@auth_router.post("/createUser")
async def create_account(name: str, email: str, password: str):
    Session = sessionmaker(bind=db)
    session = Session()
    user = session.query(User).filter(User.email==email).first()

    if user:
        return {"Message": "User already exists!"}
    else:
        new_user = User(name, email, password)
        session.add(new_user)
        session.commit()
        return {"Message": "User created!"}