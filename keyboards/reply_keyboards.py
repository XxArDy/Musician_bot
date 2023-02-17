from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Найти музику')]], resize_keyboard=True)
candy_menu_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Корзина'),
                                                     KeyboardButton(text='Вихід')]], resize_keyboard=True)

