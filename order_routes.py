from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_session, verify_token
from schemas import OrderSchema
from models import Order, User


order_router = APIRouter(prefix="/orders", tags=["orders"], dependencies=[Depends(verify_token)])

@order_router.get("/")
async def orders():
    return {"Message": "Access granted!"}

@order_router.post("/order")
async def create_order(order_schema: OrderSchema, session: Session = Depends(get_session)):
    new_order = Order(user=order_schema.user)
    session.add(new_order)
    session.commit()
    return {"Message": f"Order created! Order id: {new_order.id}"}

@order_router.post("/pedidos/cancelar/{order_id}")
async def cancel_order(order_id: int, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    order = session.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Order not found")
    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=401, detail="You don't have permission to cancel this order")
    order.status = "CANCELADO"
    session.commit()
    return {
        "Message": f"Order number: {order.id} canceled with sucess",
        "Order": order
    }