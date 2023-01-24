from database.models import Good
from webapp.webapp.user.models import CategoryByUser, AuthWebApp
from database.db import db_session


def calc_number_of_participants_for_receipt(receipt_id: int) -> int|None:
    # Подсчет количества участников вечеринки #
    set_of_users = set()
    try:
        filtered_by_receipt_id = db_session.query(CategoryByUser).filter(CategoryByUser.receipt_id == receipt_id).all() #список id записей по данному чеку
        for line in filtered_by_receipt_id:
            set_of_users.add(line.user_id) #формирование множества user_id для конкретного чека
        return len(set_of_users)
    except:
        return None    


def calc_sum_of_categories(receipt_id: int) -> dict|None:
    # Формирование словаря - категория: сумма #
    dict_sum_categories = {}
    try:
        filtered_by_receipt_id = db_session.query(Good).filter(Good.receipt_id == receipt_id).all() #список id записей по данному чеку
        for line in filtered_by_receipt_id:
            if line.category_id in dict_sum_categories:
                dict_sum_categories[line.category_id] += line.sum
            else:
                dict_sum_categories[line.category_id] = line.sum
        return dict_sum_categories
    except:
        return None


def create_dict_category_quantuty_users(receipt_id: int, category_list: list) -> dict|None: # Список из веба достаем
    quantity_entry = calc_number_of_participants_for_receipt(receipt_id)
    dict_category_quantity_users = {}
    try:
        filtered_by_receipt_id = db_session.query(CategoryByUser).filter(CategoryByUser.receipt_id == receipt_id).all() #список id записей по данному чеку
        for category in category_list:
            quantity_entry_in_func = quantity_entry
            for line in filtered_by_receipt_id:
                if category == line.category_id:
                    quantity_entry_in_func -= 1
            dict_category_quantity_users[category] = quantity_entry_in_func
        return dict_category_quantity_users
    except:
        return None


def create_dict_user_categories(receipt_id: int, category_list: list) -> dict[list]|None:
    dict_user_categories = {}
    list_of_user_ids = []
    try:
        filtered_by_receipt_id = db_session.query(CategoryByUser).filter(CategoryByUser.receipt_id == receipt_id).all() #список id записей по данному чеку
        for line in filtered_by_receipt_id:
            if line.category_id == 0:
                dict_user_categories[line.user_id] = category_list
                break
            temp_category_list = [
                category for category in category_list
            ]
            if line.user_id in list_of_user_ids:
                current_list = dict_user_categories[line.user_id]
                current_list.remove(line.category_id)
                dict_user_categories[line.user_id] = current_list
            else:
                list_of_user_ids.append(line.user_id)
                temp_category_list.remove(line.category_id)
                dict_user_categories[line.user_id] = temp_category_list
        return dict_user_categories
    except:
        return None


def calculate_user_debt(receipt_id: int, category_list: list) -> list|None: #расчет задолженности конкретного человека
    try:
        dict_user = create_dict_user_categories(receipt_id, category_list)
        dict_user_debt = {}
        list_users_debt = []
        for user_id in dict_user:
            summ = 0
            for category_id in dict_user[user_id]:
                summ += calc_sum_of_categories(receipt_id)[category_id]/create_dict_category_quantuty_users(receipt_id, category_list)[category_id]
            user = db_session.query(AuthWebApp).filter(AuthWebApp.id == user_id).first()
            dict_user_debt[user.last_name] = "{:.2f}".format(summ)
        print(dict_user_debt)
        return dict_user_debt
    except:
        return None
