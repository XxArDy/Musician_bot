from .base import Session, engine, Base
from .data import Product, Order

import os


class Database:
    # region get
    async def get_all_product(self):
        session = Session()
        products = session.query(Product).all()
        session.close()
        return products

    async def get_product_by_name(self, product_name):
        session = Session()
        product = session.query(Product).filter(Product.name == product_name).one()
        session.close()
        return product

    async def get_product_by_id(self, product_id: int):
        try:
            session = Session()
            product = session.query(Product).filter(Product.id == product_id).one()
            session.close()
            return product
        except:
            return None

    async def get_order(self, user_id: int):
        session = Session()
        product = session.query(Order).filter(Order.user_id == user_id).all()
        session.close()
        return product

    async def get_quantity(self, user_id: int, product_id: int):
        session = Session()
        product = session.query(Order).filter(Order.user_id == user_id, Order.product_id == product_id).all()
        session.close()
        return product

    async def get_one_quantity(self, user_id: int, product_id: int):
        try:
            session = Session()
            product = session.query(Order).filter(Order.user_id == user_id,
                                                  Order.product_id == product_id).one().quantity
            session.close()
            return product
        except:
            return None
    # endregion

    # region add
    async def add_order(self, user_id: int, product_id: int):
        session = Session()
        count = await self.get_one_quantity(user_id, product_id)
        if count is None:
            session.add(Order(user_id, product_id, 1))
            session.commit()
        else:
            await self.update_cart(user_id, product_id, count + 1)
        session.close()
    # endregion

    # region create
    def create_base(self):
        if os.path.exists('sweet.db'):
            os.remove('sweet.db')
        Base.metadata.create_all(engine)

    def generate_product(self):
        session = Session()
        session.add(Product("Fender picks", 20, 15,
                            "Просто неперевершені медіатори для гри на гітарі від компанії Fender."))

        session.add(Product("Gibson picks", 40, 25,
                            "Просто неперевершені медіатори для гри на гітарі від компанії Gibson."))

        session.add(Product("Procraft 34 inch", 12, 7000,
                            "Дуже крута акустична гітара з дуба.Живе і насичене звучання з характерним резонансом не "
                            "залишить байдужим навіть найвибагливішого гітариста."))

        session.add(Product("Samson G-Track", 45, 15000,
                            "Професійний звукозапис став як ніколи більш доступним з професійним USB-мікрофоном Samson "
                            "G-Track Pro."))

        session.add(Product("Samson Q2U", 180, 5000,
                            "Високоякісний мікрофон з вимикачем звуку і підставкою для виключно чистої, природної "
                            "передачі голосу."))

        session.add(Product("Sony RF995", 180, 4500,
                            "Прекрасні навушники, які наділять любого користувача неймовірно чистим звуком та "
                            "допоможуть відчути себе в іншому світі."))

        session.add(Product("Yamaha F310", 180, 6000,
                            "Живе і насичене звучання з характерним резонансом не залишить байдужим навіть "
                            "найвибагливішого гітариста."))
        session.commit()
        session.close()
    # endregion

    # region update
    async def update_cart(self, user_id: int, product_id: int, quantity: int):
        session = Session()
        cart = session.query(Order).filter(Order.user_id == user_id, Order.product_id == product_id).first()
        cart.quantity = quantity
        session.commit()
        session.close()
    # endregion

    # region delete
    async def delete_order(self, user_id: int):
        session = Session()
        session.query(Order).where(Order.user_id == user_id).delete()
        session.commit()
        session.close()

    async def remove_one_item(self, user_id: int, product_id: int):
        session = Session()
        session.query(Order).where(Order.user_id == user_id, Order.product_id == product_id).delete()
        session.commit()
        session.close()
    # endregion
