from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from database import *
from keyboards import *
from misc import DownloadMusic
from states import UserStates


class CustomUserHandlers:
    def __init__(self, bot: Bot, dispatcher: Dispatcher):
        self.database = Database()
        self.dp = dispatcher
        self.bot = bot
        self.register_event()

    def register_event(self):
        """Реєструєм команди"""
        self.dp.register_message_handler(self.start_cmd, commands=['start'])
        self.dp.register_message_handler(self.candy_cmd, commands=['shop'])

        """Реєструєм івенти на текст"""
        self.dp.register_message_handler(self.find_music, Text(equals=['Найти музику']), state=None)
        self.dp.register_message_handler(self.exit_text, Text(equals=['Вихід']))
        self.dp.register_message_handler(self.download_music, state=UserStates.state)
        self.dp.register_message_handler(self.show_cart, Text(equals=['Корзина']))

        """Реєструємо калбеки"""
        self.dp.register_callback_query_handler(self.continue_music, text='continue')
        self.dp.register_callback_query_handler(self.candy_next, callback_data.filter(action='next'))
        self.dp.register_callback_query_handler(self.candy_back, callback_data.filter(action='back'))
        self.dp.register_callback_query_handler(self.candy_add_card, callback_data.filter(action='add_to_cart'))
        self.dp.register_callback_query_handler(self.candy_back_menu, text='back_menu')
        self.dp.register_callback_query_handler(self.candy_plus, callback_data.filter(action='plus'))
        self.dp.register_callback_query_handler(self.candy_minus, callback_data.filter(action='minus'))
        self.dp.register_callback_query_handler(self.candy_remove, callback_data.filter(action='remove'))
        self.dp.register_callback_query_handler(self.candy_pay, text='pay')
        self.dp.register_callback_query_handler(self.candy_accept_pay, text='accept_pay')
        self.dp.register_callback_query_handler(self.candy_continue_buy, text='continue_buy')
        self.dp.register_callback_query_handler(self.candy_exit, text='exit')

    # region command
    async def start_cmd(self, message: types.Message):
        await self.bot.send_message(message.chat.id, f'Привіт {message.from_user.first_name}',
                                    reply_markup=start_keyboard)

    async def candy_cmd(self, message: types.Message):
        await message.reply(text='🎤🎧🎶🎸🎤🎧🎶🎸Music🎤🎧🎶🎸🎤🎧🎶🎸', reply_markup=candy_menu_keyboard)
        prod = await self.database.get_product_by_id(1)
        await self.bot.send_photo(message.chat.id, photo=open(f'pictures/{prod.name}.jpeg', 'rb'),
                                  caption=f'{prod.name}\nВага: {prod.weight} г\nЦіна: {prod.price} грн'
                                          f'\nОпис: {prod.description}', reply_markup=get_keyboard(1))

    # endregion
    # region text
    async def find_music(self, message: types.Message):
        await message.answer('Ведіть силку або напишіть назву відео з ютуба:')
        await UserStates.state.set()

    async def exit_text(self, message: types.Message):
        await self.bot.send_message(message.from_user.id, text='Повернули до музики', reply_markup=start_keyboard)

    async def download_music(self, message: types.Message, state: FSMContext):
        await state.finish()
        down = DownloadMusic(self.bot, message)
        await down.download()

    async def show_cart(self, message: types.Message):
        products = await self.database.get_order(message.from_user.id)
        keyboard = await gen_cart(products, message.from_user.id)
        text = 'Ваші товари в корзині:'
        if len(products) == 0:
            text = 'Корзина пуста'
        await self.bot.send_message(message.from_user.id, text=text, reply_markup=keyboard)

    # endregion

    # region callbacks
    async def continue_music(self, callback: types.CallbackQuery):
        await self.bot.send_message(callback.from_user.id, 'Ведіть силку або напишіть назву відео з ютуба:')
        await UserStates.state.set()

    async def candy_next(self, callback: types.CallbackQuery, callback_data: dict):
        amount = int(callback_data['amount'])
        amount += 1
        prod = await self.database.get_product_by_id(amount)
        if prod is not None:
            await callback.message.edit_media(
                media=types.InputMediaPhoto(media=open(f'pictures/{prod.name}.jpeg', 'rb'),
                                            caption=f'{prod.name}\nВага: {prod.weight} г\nЦіна: {prod.price} грн'
                                                    f'\nОпис: {prod.description}'),
                reply_markup=get_keyboard(amount))

    async def candy_back(self, callback: types.CallbackQuery, callback_data: dict):
        amount = int(callback_data['amount'])
        amount -= 1
        prod = await self.database.get_product_by_id(amount)
        if prod is not None:
            await callback.message.edit_media(
                media=types.InputMediaPhoto(media=open(f'pictures/{prod.name}.jpeg', 'rb'),
                                            caption=f'{prod.name}\nВага: {prod.weight} г\nЦіна: {prod.price} грн'
                                                    f'\nОпис: {prod.description}'), reply_markup=get_keyboard(amount))

    async def candy_add_card(self, callback: types.CallbackQuery, callback_data: dict):
        await self.database.add_order(callback.from_user.id, int(callback_data['amount']))
        amount = int(callback_data['amount'])
        await callback.message.delete_reply_markup()
        await callback.message.edit_reply_markup(get_keyboard(amount))

    async def candy_back_menu(self, callback: types.CallbackQuery):
        prod = await self.database.get_product_by_id(1)
        await self.bot.send_photo(callback.from_user.id, photo=open(f'pictures/{prod.name}.jpeg', 'rb'),
                                  caption=f'{prod.name}\nВага: {prod.weight} г\nЦіна: {prod.price} грн'
                                          f'\nОпис: {prod.description}', reply_markup=get_keyboard(1))

    async def candy_plus(self, callback: types.CallbackQuery, callback_data: dict):
        product_id = callback_data.get('amount')
        count_in_cart = await self.database.get_quantity(callback.message.chat.id, product_id)
        count = 0 if not count_in_cart else sum(j.quantity for j in count_in_cart)
        await self.database.update_cart(callback.message.chat.id, product_id, count + 1)
        data = await self.database.get_order(callback.from_user.id)
        keyboard = await gen_cart(data, callback.from_user.id)

        await callback.message.edit_reply_markup(keyboard)

    async def candy_minus(self, callback: types.CallbackQuery, callback_data: dict):
        product_id = callback_data.get('amount')
        count_in_cart = await self.database.get_quantity(callback.message.chat.id, product_id)
        count = 0 if not count_in_cart else sum(j.quantity for j in count_in_cart)
        if count == 0:
            await callback.message.answer('Товара нема')
            return 0
        elif count == 1:
            await self.database.remove_one_item(callback.message.chat.id, product_id)
            await callback.message.edit_text(text='Корзина пуста')
        else:
            await self.database.update_cart(callback.message.chat.id, product_id, count - 1)
        data = await self.database.get_order(callback.from_user.id)
        keyboard = await gen_cart(data, callback.from_user.id)

        await callback.message.edit_reply_markup(keyboard)

    async def candy_remove(self, callback: types.CallbackQuery, callback_data: dict):
        product_id = callback_data.get('amount')
        await self.database.remove_one_item(callback.from_user.id, product_id)
        count_in_cart = await self.database.get_quantity(callback.message.chat.id, product_id)
        count = 0 if not count_in_cart else sum(j.quantity for j in count_in_cart)
        if count == 0:
            await callback.message.edit_text(text='Корзина пуста')
        data = await self.database.get_order(callback.from_user.id)
        keyboard = await gen_cart(data, callback.from_user.id)

        await callback.message.edit_reply_markup(keyboard)

    async def candy_pay(self, callback: types.CallbackQuery):
        suma = 0
        products = await self.database.get_order(callback.from_user.id)
        for i in products:
            prod = await self.database.get_product_by_id(i.product_id)
            suma += i.quantity * prod.price

        await self.bot.send_message(callback.from_user.id, text=f'Ваша сума до оплати:\n{suma}грн',
                                    reply_markup=pay_keyboard)

    async def candy_accept_pay(self, callback: types.CallbackQuery):
        await self.database.delete_order(callback.from_user.id)
        await self.bot.send_message(callback.from_user.id, text='Ви успішно оплатили покупку!',
                                    reply_markup=continue_buy)

    async def candy_continue_buy(self, callback: types.CallbackQuery):
        prod = await self.database.get_product_by_id(1)
        await self.bot.send_photo(callback.from_user.id, photo=open(f'pictures/{prod.name}.jpeg', 'rb'),
                                  caption=f'{prod.name}\nВага: {prod.weight} г\nЦіна: {prod.price} грн'
                                          f'\nОпис: {prod.description}', reply_markup=get_keyboard(1))

    async def candy_exit(self, callback: types.CallbackQuery):
        await self.bot.send_message(callback.from_user.id, text='Повернули до музики', reply_markup=start_keyboard)

# endregion
