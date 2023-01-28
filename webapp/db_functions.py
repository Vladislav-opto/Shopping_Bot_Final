from datetime import datetime
from database.models import Category
from webapp.webapp.model import db
from webapp.webapp.user.models import AuthWebApp, CategoryByUser, AuthCodeByUser


def create_user(first_name: str, last_name: str, email: str) -> None:
    """
    Save the user to the database.
    """

    user = [{'first_name': first_name, 'last_name': last_name, 'email': email}]
    db.session.bulk_insert_mappings(AuthWebApp, user)
    db.session.commit()


def create_user_choice(select_category: list, email: str, authorization_code: str) -> bool:
    user = AuthWebApp.query.filter(AuthWebApp.email == email).first()
    date_time_now = datetime.now()
    if select_category == ['Скидываюсь на все']:
        user_choice = [{'user_id': user.id, 'category_id': 0, 'upload': date_time_now.strftime('%Y-%m-%d %H:%M:%S'), 'receipt_id': authorization_code}]
        db.session.bulk_insert_mappings(CategoryByUser, user_choice)
        db.session.commit()
    elif 'Скидываюсь на все' in select_category:
        return False
    else:
        for category in select_category:
            category_data = Category.query.filter(Category.name == category).first()
            user_choice = [{'user_id': user.id, 'category_id': category_data.id, 'upload': date_time_now.strftime('%Y-%m-%d %H:%M:%S'), 'receipt_id': authorization_code}]
            db.session.bulk_insert_mappings(CategoryByUser, user_choice)
            db.session.commit()
    return True

def create_auth_code_by_id(authorization_code: str, id: int) -> None:
    date_time_now = datetime.now()
    auth_code = [{'user_id': id, 'auth_code': authorization_code, 'upload': date_time_now.strftime('%Y-%m-%d %H:%M:%S')}]
    db.session.bulk_insert_mappings(AuthCodeByUser, auth_code)
    db.session.commit()

