from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def auth():
    """
    Essa é a rota padrão de autenticação da API!
    """
    return {"Message": "Access granted!", "Authenticated": False}