from fastapi import Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session
from main import oauth2_scheme, SECRET_KEY, ALGORITHM
from models import db, Usuario
from jose import jwt, JWTError

def get_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()

def verify_token(session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    usuario = session.query(Usuario).filter(Usuario.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário Inválido")
    return usuario