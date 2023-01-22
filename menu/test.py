from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater, 
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler)

from data.models import Receipt

FIRST, SECOND = range(2)


def keyboard():
    reply_keyboard = [
        [InlineKeyboardButton('<<<', callback_data='0'), InlineKeyboardButton('>>>', callback_data='1')],
    ]

    return InlineKeyboardMarkup(reply_keyboard, resize_keyboard=True)


def start(update, context):
    context.user_data['counter'] = 0
    receipt_list = []
    for receipt in Receipt.query.filter(Receipt.tg_user_id == '16'):
        receipt_list.append([receipt.name, receipt.receipt_date, receipt.id])
    if receipt_list:
        context.user_data['receipt_list'] = receipt_list
        receipt_info = context.user_data.get('receipt_list')
        text=(f'Магазин: {receipt_info[0][0]}'
                f'\nДата покупки: {receipt_info[0][1]}'
                f'\nКод авторизации: {receipt_info[0][2]}')
        update.message.reply_text(
            text,
            reply_markup=keyboard()
        )

        return FIRST

    else:
        update.message.reply_text('У вас нет загруженных чеков 😔')


def increment(update, context):
    query = update.callback_query
    bot = context.bot
    receipt_info = context.user_data.get('receipt_list')
    counter = context.user_data.get('counter')
    counter += 1
    try:
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text=(f'Магазин: {receipt_info[counter][0]}'
                  f'\nДата покупки: {receipt_info[counter][1]}'
                  f'\nКод авторизации: {receipt_info[counter][2]}'),
            reply_markup=keyboard()
        )
    except IndexError:
        counter = 0
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text=(f'Магазин: {receipt_info[counter][0]}'
                  f'\nДата покупки: {receipt_info[counter][1]}'
                  f'\nКод авторизации: {receipt_info[counter][2]}'),
            reply_markup=keyboard()
        )

    context.user_data['counter'] = counter


def decrement(update, context):
    query = update.callback_query
    bot = context.bot
    receipt_info = context.user_data.get('receipt_list')
    counter = context.user_data.get('counter')
    counter -= 1
    try:
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text=(f'Магазин: {receipt_info[counter][0]}'
                  f'\nДата покупки: {receipt_info[counter][1]}'
                  f'\nКод авторизации: {receipt_info[counter][2]}'),
            reply_markup=keyboard()
        )
    except IndexError:
        counter = len(receipt_info) - 1
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text=(f'Магазин: {receipt_info[counter][0]}'
                  f'\nДата покупки: {receipt_info[counter][1]}'
                  f'\nКод авторизации: {receipt_info[counter][2]}'),
            reply_markup=keyboard()
        )

    context.user_data['counter'] = counter


def main():
    updater = Updater(
        '5624223735:AAGYPA9pp6UiWOEvVrDhQYGlF-isWXzjn-w', use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST: [CallbackQueryHandler(decrement, pattern='^'+str(0)+'$'),
                    CallbackQueryHandler(increment, pattern='^'+str(1)+'$')]
        },
        fallbacks=[CommandHandler('start', start)]
    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
