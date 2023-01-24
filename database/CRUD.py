from database.db import db_session
from database.models import Receipt, Good, Category, CategoryTriggers
from datetime import datetime
from typing import Any


def add_receipt(receipt_name: str, userid: int) -> int:
    date_time_now = datetime.now()
    receipt = Receipt(name=receipt_name, user_id=userid, date_upload=date_time_now.strftime('%Y-%m-%d %H:%M'))
    db_session.add(receipt)
    db_session.commit()
    return receipt.id


def get_receipt(receipt_id: int) -> str | None:
    if db_session.query(
        Receipt.query.filter(Receipt.id == receipt_id).exists()
                                                              ).scalar():
        return Receipt.query.get(receipt_id)
    else:
        return None


def add_receipt_content(receipt_content: list, receipt_id: int) -> None:
    for good in receipt_content:
        good['receipt_id'] = receipt_id
    db_session.bulk_insert_mappings(Good, receipt_content)
    db_session.commit()


def get_receipt_content(receipt_id: int) -> str | None:
    if db_session.query(
        Good.query.filter(Good.id == receipt_id).exists()
                                                        ).scalar():
        return Good.query.get(receipt_id)
    else:
        return None


def add_category(categories: dict) -> None:
    list_categories = []
    for name_category in categories:
        temp_dict = {}
        temp_dict['name'] = name_category
        list_categories.append(temp_dict)
    db_session.bulk_insert_mappings(Category, list_categories)
    db_session.commit()
    return [id[0] for id in Category.query.with_entities(Category.id).all()]


def add_triggers(categories: dict[str,list], list_of_ids: list[int]) -> None:
    list_to_db = []
    for index, list_triggers in enumerate(categories.values()):
        for trigger in list_triggers:
            temp_dict = {}
            temp_dict['name'] = trigger
            temp_dict['category_id'] = list_of_ids[index]
            list_to_db.append(temp_dict)
    db_session.bulk_insert_mappings(CategoryTriggers, list_to_db)
    db_session.commit()


def get_category(trigger: tuple[str]) -> list[str]:
    query = db_session.query(Category, CategoryTriggers).join(
        Category, CategoryTriggers.category_id == Category.id
    ).filter(CategoryTriggers.name == trigger)
    for category, _ in query:
        break
    return [category.id, category.name]
    

def check_empty_table() -> bool:
    if db_session.query(Category).first():
        return False
    else:
        return True


def get_triggers_name() -> Any:
    return db_session.query(CategoryTriggers.name)
