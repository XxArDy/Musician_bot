from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from database import Database

callback_data = CallbackData('vote', 'action', 'amount')

continue_keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(text='Продовжити', callback_data='continue'))

pay_keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(text='Оплатити', callback_data='accept_pay'))
continue_buy = InlineKeyboardMarkup().add(InlineKeyboardButton(text='Продовжити покупку',
                                                               callback_data='continue_buy')).add(InlineKeyboardButton(text='Вихід',
                                                              callback_data='exit'))


def get_keyboard(amount):
    return InlineKeyboardMarkup() \
        .add(InlineKeyboardButton(text='⬅️', callback_data=callback_data.new(action='back',
                                                                             amount=amount)),
             InlineKeyboardButton(text='В корзину', callback_data=callback_data.new(action='add_to_cart',
                                                                                    amount=amount)),
             InlineKeyboardButton(text='➡️', callback_data=callback_data.new(action='next',
                                                                             amount=amount)))


async def gen_cart(data, user_id):
    database = Database()
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    for i in data:
        prod_id = i.product_id
        prod = await database.get_product_by_id(prod_id)
        count = await database.get_quantity(user_id, prod_id)
        count = 0 if not count else sum(j.quantity for j in count)
        keyboard.add(InlineKeyboardButton(text=f'{prod.name}: {prod.price} грн - {count}шт',
                                          callback_data=callback_data.new(action='plus', amount=prod_id)))
        keyboard.add(InlineKeyboardButton(text='🔼',
                                          callback_data=callback_data.new(action='plus', amount=prod_id)),
                     InlineKeyboardButton(text='🔽',
                                          callback_data=callback_data.new(action='minus', amount=prod_id)),
                     InlineKeyboardButton(text='❌', callback_data=callback_data.new(action='remove', amount=prod_id)))
    if data:
        keyboard.add(InlineKeyboardButton(text='Оплатити', callback_data='pay'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='back_menu'))
    return keyboard
