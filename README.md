# Проект ShoppingBot (дипломный проект ЛТЛ)

ShoppingBot - телеграмм-бот, который помогает рассчитать долг каждого участника вечеринки.

## Установка

1. Клонируйте репозиторий с github (`git clone`)
2. Создайте виртуальное окружение (`python -m venv env`)
3. Установите зависимости `pip install -r requirements.txt`
4. Откройте файл `settings.py` в папке `setting_box`.
5. Впишите в `settings.py` следующее: (`находится в разработке`)
```
API_KEY = 'API-ключ бота'
URL = 'Ссылка на базу данных'
USER_EMOJI = [":shit:", ":smile:", ":sunglasses:", ":eyes:"]
```
6. Запустите две командные строки.
7. В каждой из них перейдите в папку с проектом (cd `путь до проекта на вашем ПК`)
8. В первой командной строке запустите `bot_and_db.py` (`python bot_and_db.py`)
9. Во второй командной строке запустите `web.py` (`python web.py`)

### Структура базы данных в проекте

![Говорите и пишите по-русски правильно](https://raw.githubusercontent.com/Vladislav-opto/Shopping_Bot_Final/main/images/bd_structure.JPG)
