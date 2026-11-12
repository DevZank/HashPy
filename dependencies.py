from fastapi import Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session
from main import SECRET_KEY
from models import db, User
from jose import jwt, JWTError

def get_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session # Não encerra a função mais igual o return faz
    finally: # Independente do que acontecer no try esse bloco é executado
        session.close()

"""
def verify_token(session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid User")
    return user
"""