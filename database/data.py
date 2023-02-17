from sqlalchemy import ForeignKey, Column, String, Integer, Boolean
from sqlalchemy.orm import relationship

from .base import Base
import typing
import sqlalchemy as sa


class Product(Base):
    __tablename__ = "products"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("product_name", String)
    weight = Column("weight", Integer)
    price = Column("price", Integer)
    description = Column("description", String)

    def __init__(self, name, weight: int, price: int, description):
        self.name = name
        self.weight = weight
        self.price = price
        self.description = description

    def __repr__(self) -> str:
        return self._repr(id=self.id, name=self.name, weight=self.weight,
                          price=self.price, description=self.description)

    def _repr(self, **fields: typing.Dict[str, typing.Any]) -> str:
        field_strings = []
        at_least_one_attached_attribute = False
        for key, field in fields.items():
            try:
                field_strings.append(f'{key}={field!r}')
            except sa.orm.exc.DetachedInstanceError:
                field_strings.append(f'{key}=DetachedInstanceError')
            else:
                at_least_one_attached_attribute = True
        if at_least_one_attached_attribute:
            return f"<{self.__class__.__name__}({','.join(field_strings)})>"
        return f"<{self.__class__.__name__} {id(self)}>"


class Order(Base):
    __tablename__ = "orders"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    user_id = Column("user_id", Integer)
    product_id = Column("product_id", Integer, ForeignKey("products.id"))
    product = relationship("Product", uselist=False)
    quantity = Column("quantity", Integer)

    def __init__(self, user_id: int, product_id: int, quantity: int):
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity

    def __repr__(self) -> str:
        return self._repr(id=self.id, product_id=self.product_id, user_id=self.user_id,
                          quantity=self.quantity)

    def _repr(self, **fields: typing.Dict[str, typing.Any]) -> str:
        field_strings = []
        at_least_one_attached_attribute = False
        for key, field in fields.items():
            try:
                field_strings.append(f'{key}={field!r}')
            except sa.orm.exc.DetachedInstanceError:
                field_strings.append(f'{key}=DetachedInstanceError')
            else:
                at_least_one_attached_attribute = True
        if at_least_one_attached_attribute:
            return f"<{self.__class__.__name__}({','.join(field_strings)})>"
        return f"<{self.__class__.__name__} {id(self)}>"

