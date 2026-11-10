from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType

# Cria a conexão do seu banco
db = create_engine("sqlite:///banco.db")

# Cria a base do banco de dados
Base = declarative_base()

# Cria as classes/tabelas do banco

# Usuarios
class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String, nullable=False)
    email = Column("email", String, nullable=False)
    password = Column("password", String, nullable=False)
    active = Column("active", Boolean, default=True)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, name, email, password, active=True, admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.active = active
        self.admin = admin

# Pedidos
class Order(Base):
    __tablename__ = "orders"

    """
        ORDER_STATUS = (
           ("PENDENTE", "PENDENTE"),
           ("CANCELADO", "CANCELADO"),
           ("FINALIZADO", "FINALIZADO")
        )
    """

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String, nullable=False) # Pendente, Cancelado, Finalizado
    user = Column("user", ForeignKey("users.id"), nullable=False)
    price = Column("price", Float, nullable=False)
    # items =

    def __init__(self, user, status="PENDENTE", price=0):
        self.user = user
        self.price = price
        self.status = status

# Itens Pedido
class OrderItems(Base):
    __tablename__ = "order_items"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantity = Column("quantity", Integer)
    tasty = Column("tasty", String)
    size = Column("size", String)
    unit_price = Column("unit_price", Float)
    order = Column("order", ForeignKey("orders.id"))

    def __init__(self, quantity, tasty, size, unit_price, order):
        self.quantity = quantity
        self.tasty = tasty
        self.size = size
        self.unit_price = unit_price
        self.order = order

# Executa a criação dos metadados do seu banco (Cria efetivamente o banco de dados)