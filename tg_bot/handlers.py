import os
from random import choice
from telegram import (
    ReplyKeyboardMarkup, ReplyKeyboardRemove, Update,
    InlineKeyboardMarkup, InlineKeyboardButton,
)
from telegram.ext import ConversationHandler, CallbackContext

from processing_qr_code.API_FNS.nalog_ru import NalogRuPython
from qr_code_scan_opencv.QR_to_string_openCV import read_qr_code
from processing_qr_code.receipt import treat_receipt
from settings_box import settings
from database import CRUD
from categorization.utils import json_func
from categorization.categorization import add_categories_to_receipt
from database.models import Receipt
from tg_bot.utils.keyboard import inline_keyboard, back_to_menu
from calc_debt.calc_debt import calculate_user_debt
from database.models import Good


def greet_user(update: Update, context) -> int:
    """Начало разговора."""
    reply_keyboard = [['Привет 👋']]
    user_name = update.message.chat.first_name
    message = f'Привет <b>{user_name}</b>!'
    update.message.reply_text(
        f'{message}', parse_mode='html',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, resize_keyboard=True,
        ),
    )

    return settings.MAIN_MENU


def main_menu(update: Update, context) -> int:
    """Представляет бота пользователю."""
    reply_keyboard = [
        ['Операции с чеками 💰'],
        ['У меня есть код авторизации 📢'],
        ['Хочу узнать кто сколько должен 🤑']
    ]

    update.message.reply_text(
        'Я бот Толян 🤖.\nЯ умею составлять списки покупок 🛒'
        '\nи распределять чеки.🙎‍♂️🧾👫',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, resize_keyboard=True,
        ),
    )

    return settings.ACTIONS_WITH_THE_RECEIPT


def operations_with_receipt(update: Update, context) -> int:
    """Представляет пользователю меню для работы с чеками."""
    reply_keyboard = [
        ['Добавить чек 🆕', 'Мои чеки 📑'],
        ['Возврат в предыдущее меню ↩️'],
    ]
    update.message.reply_text(
        'Выбери категорию 🔎',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, resize_keyboard=True,
        ),
    )

    return settings.MENU_RECEIPT


def add_receipt(update: Update, context) -> int:
    """Представляет пользователю меню для добавления чека."""
    answer = choice(settings.BOT_ANSWERS)
    update.message.reply_text(
        f'{answer}',
        reply_markup=back_to_menu(),
        )

    return settings.ADD_CHECK


def check_user_photo(update: Update, context: CallbackContext) -> int:
    """
    Проверяет является ли фото присланное пользователем чеком,
    если да, то сохраняет его директорию в content.user_data,
    и просит пользователя прислать номер телефона.
    """
    update.message.reply_text('Обрабатываю фото...')
    os.makedirs('tg_bot/downloads', exist_ok=True)
    photo_file = context.bot.getFile(update.message.photo[-1].file_id)
    file_name = os.path.join('tg_bot/downloads', f'{update.message.photo[-1].file_id}.jpg')
    photo_file.download(file_name)
    if read_qr_code(file_name):
        update.message.reply_text(
            'Обнаружен чек, добавляю фото в библиотеку.',
        )
        os.makedirs('tg_bot/images', exist_ok=True)
        new_filename = os.path.join('tg_bot/images', f'check_{photo_file.file_id}.jpg')
        os.rename(file_name, new_filename)
        context.user_data['file_directory'] = new_filename
        update.message.reply_text('Пожалуйста введите номер\nв формате +79ХХХХХХХХХ.')

        return settings.PHONE_NUMBER

    else:
        os.remove(file_name)
        update.message.reply_text('Чек на фото не обнаружен.')


def operation_phone_number(update: Update, context: CallbackContext) -> int:
    """
    Проверяет является ли сообщения пользователя номером телефона
    и сохраняет его в content.user_data, затем
    отправляет его в налоговую для получения кода.
    """
    if len(update.message.text) != 12 or update.message.text[:2] != '+7' or not update.message.text[1:].isdigit():
        update.message.reply_text('Введите номер телефона в формате +79ХХХХХХХХХ.')

        return settings.PHONE_NUMBER

    phone = update.message.text
    context.user_data['phone'] = phone
    update.message.reply_text('Телефон сохранен.')
    phone = NalogRuPython(context.user_data.get('phone'))
    phone.sends_sms_to_the_user()
    update.message.reply_text('Пожалуйста введите код из SMS.')
    
    return settings.CODE


def authorization_with_code(update: Update, context: CallbackContext) -> None:
    """
    Принимает от пользователя код из смс и отпровляет его в налоговую.
    """
    value = update.message.text
    phone = NalogRuPython(context.user_data.get('phone'), code=value)
    server_response = phone.sends_code_to_nalog()
    if server_response:
        string_from_qr = read_qr_code(context.user_data.get('file_directory'))
        receipt = phone.get_ticket(string_from_qr)
        phone.refresh_token_function()
        if CRUD.check_empty_table():
            list_of_ids = CRUD.add_category(json_func.read('categorization/categories.ini'))
            CRUD.add_triggers(json_func.read('categorization/categories.ini'), list_of_ids)
        processed_check = treat_receipt(receipt)
        last_receipt_id = CRUD.add_receipt(processed_check['seller'], update.message.chat.id)
        CRUD.add_receipt_content(add_categories_to_receipt(processed_check)['positions'], last_receipt_id)
        update.message.reply_text('Ваш чек добавлен и располагается в меню "Мои чеки"')
    else:
        update.message.reply_text('Введен неверный код. Пожалуйста введите код из SMS.')


def my_receipts(update: Update, context) -> None:
    """
    Открывает пользователю меню с его сохраненными чеками.
    """
    context.user_data['counter'] = 0
    receipt_list = []
    for receipt in Receipt.query.filter(Receipt.user_id == update.message.chat.id):
        receipt_list.append([receipt.name, receipt.date_upload, receipt.id])
    if receipt_list:
        context.user_data['receipt_list'] = receipt_list
        receipt_info = context.user_data.get('receipt_list')
        text=(f'Магазин: {receipt_info[0][0]}'
                f'\nДата загрузки чека: {receipt_info[0][1]}'
                f'\nКод авторизации: {receipt_info[0][2]}')
        update.message.reply_text(
            text,
            reply_markup=inline_keyboard()
        )

    else:
        update.message.reply_text('У вас нет загруженных чеков 😔')


def next_receipt(update: Update, context) -> None:
    """Выбор следующего чека в меню 'Мои чеки'."""
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
                  f'\nДата загрузки чека: {receipt_info[counter][1]}'
                  f'\nКод авторизации: {receipt_info[counter][2]}'),
            reply_markup=inline_keyboard()
        )
    except IndexError:
        counter = 0
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text=(f'Магазин: {receipt_info[counter][0]}'
                  f'\nДата загрузки чека: {receipt_info[counter][1]}'
                  f'\nКод авторизации: {receipt_info[counter][2]}'),
            reply_markup=inline_keyboard()
        )

    context.user_data['counter'] = counter


def previous_receipt(update: Update, context) -> None:
    """Выбор предыдущего чека в меню 'Мои чеки'."""
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
                  f'\nДата загрузки чека: {receipt_info[counter][1]}'
                  f'\nКод авторизации: {receipt_info[counter][2]}'),
            reply_markup=inline_keyboard()
        )
    except IndexError:
        counter = len(receipt_info) - 1
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text=(f'Магазин: {receipt_info[counter][0]}'
                  f'\nДата загрузки чека: {receipt_info[counter][1]}'
                  f'\nКод авторизации: {receipt_info[counter][2]}'),
            reply_markup=inline_keyboard()
        )

    context.user_data['counter'] = counter


def web_app(update: Update, context) -> None:
    """Открывает веб-приложение, при нажатии на кнопку."""
    reply_keyboard = [
        [InlineKeyboardButton('Вперед к новым платежам 🚀', url='http://127.0.0.1:5000')],
    ]

    update.message.reply_text('Узнай сколько потратил ты!', reply_markup=InlineKeyboardMarkup(
        reply_keyboard, resize_keyboard=True,
    ))


def tell_check_id(update: Update, context) -> int:
    """Запрашивает у пользователя номер чека."""
    update.message.reply_text(
        'Введите код авторизации интересующего вас чека.', reply_markup=back_to_menu())

    return settings.RECEIPT_DEBTORS


def show_debtors_for_user(update: Update, context) -> None:
    """Выводит информацию о должниках по чеку."""
    receipt_id = int(update.message.text)
    category_set = {_.category_id for _ in Good.query.filter(Good.receipt_id == receipt_id).all()}
    category_list = list(category_set)
    dict_of_debtors = calculate_user_debt(receipt_id, category_list)
    message_for_user = ''
    if dict_of_debtors:
        message_for_user += f'Информация по чеку: {receipt_id}'
        message_for_user += f'\n---'
        for person, debt in dict_of_debtors.items():
            message_for_user += f'\n{person}: {debt} руб.'
        message_for_user += f'\n---'
        message_for_user += f'\nРасчеты верны, если все участники чека авторизировались.'
    else:
        message_for_user += f'Никто из участников вечеринки не прошел авторизацию 😔'
    update.message.reply_text(message_for_user, reply_markup=back_to_menu())


def cancel(update: Update, context) -> int:
    """Заканчивает беседу."""
    update.message.reply_text(
        'До Встречи!', reply_markup=ReplyKeyboardRemove()
    )
    
    return ConversationHandler.END
