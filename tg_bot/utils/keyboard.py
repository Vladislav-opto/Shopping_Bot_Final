from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup


def inline_keyboard():
    """Выводит клавиатуру для меню 'Мои чеки'"""
    reply_keyboard = [
        [InlineKeyboardButton('<<<', callback_data='0'), InlineKeyboardButton('>>>', callback_data='1')],
    ]

    return InlineKeyboardMarkup(reply_keyboard, resize_keyboard=True)


def back_to_menu():
    """Выводит клавиатуру для меню 'Возврат в предыдущее меню'"""
    reply_keyboard = [
        ['Возврат в предыдущее меню ↩️'],
    ]

    return ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)