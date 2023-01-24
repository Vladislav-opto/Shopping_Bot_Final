from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def keyboard():
    reply_keyboard = [
        [InlineKeyboardButton('<<<', callback_data='0'), InlineKeyboardButton('>>>', callback_data='1')],
    ]

    return InlineKeyboardMarkup(reply_keyboard, resize_keyboard=True)