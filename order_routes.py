from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_session, verify_token
from schemas import OrderSchema, OrderItemSchema
from models import Order, User, OrderItems


order_router = APIRouter(prefix="/orders", tags=["orders"], dependencies=[Depends(verify_token)])

@order_router.get("/")
async def orders_route():
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

@order_router.get("/listar")
async def list_orders(session: Session = Depends(get_session), user: User = Depends(verify_token)):
    if not user.admin:
        raise HTTPException(status_code=400, detail="You haven't authorization to access this rote")
    else:
        orders = session.query(Order).all()
        return {
            "orders": orders
        }

@order_router.post("/order/add-item/{order_id}")
async def add_order_item(order_id: int, order_item_schema: OrderItemSchema, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    order = session.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Order not exists")
    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=401, detail="You haven't authorization to access this rote")
    order_item = OrderItems(order_item_schema.quantity, order_item_schema.tasty, order_item_schema.size, order_item_schema.unit_price, order_id)
    session.add(order_item)
    order.calculate_price()
    session.commit()
    return {
        "Message": "Item created!",
        "item_id": order_item.id,
        "order_price": f"{order.price:.2f}"
    }