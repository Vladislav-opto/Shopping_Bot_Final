from database.models import Good
from webapp.webapp.user.models import CategoryByUser, AuthWebApp
from database.db import db_session


def calc_number_of_participants_for_receipt(receipt_id: int) -> int|None:
    """Подсчет количества участников вечеринки"""
    set_of_users = set()
    try:
        filtered_by_receipt_id = db_session.query(CategoryByUser).filter(CategoryByUser.receipt_id == receipt_id).all()
        for line in filtered_by_receipt_id:
            set_of_users.add(line.user_id)
        return len(set_of_users)
    except:
        return None    


def calc_sum_of_categories(receipt_id: int) -> dict|None:
    """Формирование словаря - категория: сумма """
    dict_sum_categories = {}
    try:
        filtered_by_receipt_id = db_session.query(Good).filter(Good.receipt_id == receipt_id).all()
        for line in filtered_by_receipt_id:
            if line.category_id in dict_sum_categories:
                dict_sum_categories[line.category_id] += line.sum
            else:
                dict_sum_categories[line.category_id] = line.sum
        return dict_sum_categories
    except:
        return None


def create_dict_category_quantuty_users(receipt_id: int, category_list: list) -> dict|None:
    """Подсчет количества выбраных категорий пользователями"""
    quantity_entry = calc_number_of_participants_for_receipt(receipt_id)
    dict_category_quantity_users = {}
    try:
        filtered_by_receipt_id = db_session.query(CategoryByUser).filter(CategoryByUser.receipt_id == receipt_id).all()
        for category in category_list:
            counter = 0
            quantity_entry_in_func = quantity_entry
            for line in filtered_by_receipt_id:
                if category == line.category_id:
                    quantity_entry_in_func -= 1
                    counter += 1
                elif line.category_id == 0:
                    counter += 1
            dict_category_quantity_users[category] = counter
        return dict_category_quantity_users
    except:
        return None


def create_dict_user_categories(receipt_id: int, category_list: list) -> dict[list]|None:
    """"Привязка выбранных категорий к пользователю"""
    dict_user_categories = {}
    list_of_user_ids = []
    temp_category_list = []
    try:
        filtered_by_receipt_id = db_session.query(CategoryByUser).filter(CategoryByUser.receipt_id == receipt_id).all()
        for line in filtered_by_receipt_id:
            if list_of_user_ids:
                if line.user_id != list_of_user_ids[-1]:
                    temp_category_list = []
            if line.category_id == 0:
                dict_user_categories[line.user_id] = category_list
                continue
            if line.user_id in list_of_user_ids:
                temp_category_list.append(line.category_id)
                dict_user_categories[line.user_id] = temp_category_list
            else:
                list_of_user_ids.append(line.user_id)
                temp_category_list.append(line.category_id)
                dict_user_categories[line.user_id] = temp_category_list
        return dict_user_categories
    except:
        return None


def calculate_user_debt(receipt_id: int, category_list: list) -> list|None:
    """Расчет задолженности конкретного человека"""
    try:
        dict_user = create_dict_user_categories(receipt_id, category_list)
        dict_user_debt = {}
        for user_id in dict_user:
            summ = 0
            for category_id in dict_user[user_id]:
                summ += calc_sum_of_categories(receipt_id)[category_id]/create_dict_category_quantuty_users(receipt_id, category_list)[category_id]
            user = db_session.query(AuthWebApp).filter(AuthWebApp.id == user_id).first()
            dict_user_debt[user.last_name] = "{:.2f}".format(summ)
        return dict_user_debt
    except:
        return None
