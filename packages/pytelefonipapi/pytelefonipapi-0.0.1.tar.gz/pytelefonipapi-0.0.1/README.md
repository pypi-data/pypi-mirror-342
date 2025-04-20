# pytelefonipapi - Python services for convenient work with telefon-ip.ru api

![](https://www.python.org/static/img/python-logo.png) 

Установка
============

Пользуем pip:
    
```
pip install pytelefonipapi
```

Зависимости
    
    python>=3.10
    requests
    pydantic>=2.9.2

    
Как использовать
============
Все названия методов соответствуют action в ссылке (смотрите документацию).
**Пример названия метода:** 

- _api/v1/authcalls/\<token\>/**get_code**/\<phone\>/ - `get_code`_

**Варианты импорта**
Вы можете импортировать 
    
    TelefonIpAPI - с всеми доступными методами 
    SettingAPI - только методы для работы с аккаунтом
    FlashCallsAPI - только запросы кода авторизации
    BackCallsAPI - только запрос обратной авторизации
    TGCodeAPI - только запрос кода в Telegram
    SMSCodeAPI - только запрос sms 

Так же прошу вас обратить **внимание** на аннотацию типов аргументов 

Если вам нужно чтобы ответ был в dict - то при инициализации укажите аргумент **return_dict** = True
    
    api = TelefonIpAPI(token, return_dict=True)

    # Либо
    api = TelefonIpAPI(token,)
    api.return_dict = True

Example
============
    import logging
    from datetime import datetime
    from pytelefonipapi import TelefonIpAPI, FlashCallsAPI, SettingAPI
    
    TOKEN = ""
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
    
    # Получаем биллинг файлом 
    api = TelefonIpAPI(token=TOKEN, debug=True, logger=logger)
    api.get_billing_csv(datetime.now(), "./files/", "1.csv")
    # #api.get_billing_csv("2025-04-19", "./files/", "1.csv")
    
    api_flash_calls = FlashCallsAPI(token=TOKEN, debug=True, logger=logger)
    # print(api.get_code(phone="+79969307003",))
    
    api_settings = SettingAPI(token=TOKEN, debug=True, logger=logger)
    balance = api_settings.get_balance()

