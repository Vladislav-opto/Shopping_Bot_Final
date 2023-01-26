from database.CRUD import get_category, get_triggers_name


def define_category(good: dict) -> list[int, str]:
    result_category = None
    good_without_separator = good['name'].replace('.', ' ').replace(',', ' ').replace('/', ' ')
    good_as_list = good_without_separator.lower().split()
    for category_words in get_triggers_name():     
        if category_words[0] in good_as_list:
            result_category = get_category(category_words[0])
            break
    return result_category


def add_categories_to_receipt(receipt: dict) -> dict:
    for good in receipt['positions']:
        good['category_id'], good['category_name'] = define_category(good)
    return receipt
