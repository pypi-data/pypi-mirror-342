import datetime
import json
import os
import re
import pathlib
import logging
import requests
from enum import Enum
from typing import Any

from pytelefonipapi.models import GetCodeModel, GetSMSCodeModel, GetTGCodeModel, ReverseAuthPhoneGetModel, \
    ReverseAuthPhonePostModel, ReverseAuthPhoneCheckModel, GetStatusModel, GetBalanceModel, GetBillingModel
from pytelefonipapi.exception import SetSession, TokenException


class BaseAPI:
    DEFAULT_TIMEOUT = "15"

    class RequestMethod(Enum):
        GET = "Get"
        POST = "Post"

    def __init__(self, token: str, session: requests.Session | None = None, debug: bool = False,
                 base_url: str = None, base_headers: dict = None, logger:
        logging.Logger | None = None, return_dict: bool = False):
        """

        :param token: token for access api
        :param session: session object
        :param debug: logging dict response
        :param base_url: url server api
        :param base_headers: base header for request
        :param logger: your object Logger
        :param return_dict: return a dictionary instead of models
        """

        if session is not None:
            self.__session = session
        else:
            self.__session = requests.Session()

        self.__token: str = token
        self.__debug = debug
        self.__return_dict = return_dict
        self.logger = logger if logger is not None else logging.getLogger()

        self.__base_url = "https://api.telefon-ip.ru/api/v1" if base_url is None else base_url
        self.__headers = {
            "Content-Type": "application/json",
            "Timeout": "45",
        } if base_headers is None else base_headers
        self.__last_data = None

    @property
    def session_s(self) -> requests.Session:
        """Вывести сессию"""
        return self.__session

    @session_s.setter
    def session_s(self, session: requests.Session = None):
        """Изменение сессии"""
        if session is None:
            raise SetSession(
                self.__class__.__qualname__,
                self.session_s.__name__,
                f"Не присвоен объект типа requests.Session")
        else:
            self.__session = session

    @property
    def token(self) -> str:
        return self.__token

    @token.setter
    def token(self, value: str):
        self.__token = value

    @property
    def base_url(self):
        return self.__base_url

    @base_url.setter
    def base_url(self, value: str):
        self.__base_url = value

    @property
    def headers(self):
        return self.__headers

    @headers.setter
    def headers(self, value: str):
        self.__headers = value

    @property
    def return_dict(self):
        return self.__return_dict

    @return_dict.setter
    def return_dict(self, value: str):
        self.__return_dict = value

    @headers.setter
    def headers(self, value: str):
        self.__return_dict = value

    @property
    def timeout(self):
        return self.__headers.get("Timeout")

    @timeout.setter
    def timeout(self, value: int):
        self.__headers.update({"Timeout": str(value)})

    @timeout.deleter
    def timeout(self):
        self.__headers.update({"Timeout": str(self.DEFAULT_TIMEOUT)})

    def _validate_phone_number(
        self,
        phone: str,
        country_code_format: str | None = None,  # Варианты: "+7", "7", "8", "None"
        re_sub_pattern: str = r'(\d{3})(\d{3})(\d{2})(\d{2})',
        re_sub_repl: str = r'(\1) \2-\3-\4'
    ) -> str | None:
        """
        Форматирует российский номер телефона в единый вид с указанием кода страны.

        Параметры:
            phone (str): Номер телефона в любом формате.
            country_code_format (str): Желаемый формат кода страны ("+7", "7", "8", "None").
            re_sub_pattern (str):
            re_sub_repl (str):
        Возвращает:
            str: Отформатированный номер в зависимости от re_sub_repl.
            None: Если номер некорректный.
        """
        # Удаляем все нецифровые символы
        cleaned = re.sub(r'[^\d]', '', phone)

        # Проверяем длину номера и начало
        if len(cleaned) == 10:
            # Номер без кода страны (допустим, начинается с 9)
            digits = cleaned
        elif len(cleaned) == 11 and cleaned[0] == '8':
            # Номер с 8 в начале → заменяем 8 на 7
            digits = cleaned[1:]
        elif len(cleaned) == 11 and cleaned[0] == '7':
            # Номер с 7 в начале
            digits = cleaned[1:]
        else:
            # Некорректный номер
            raise ValueError("Некорректный номер")

        # Проверяем, что оставшиеся цифры валидны (10 символов, начинаются с 9)
        if not re.fullmatch(r'[89]\d{9}', digits):
            raise ValueError("Некорректный номер")

        # Форматируем код страны в нужный вид
        if country_code_format == "+7":
            prefix = "+7"
        elif country_code_format == "7":
            prefix = "7"
        elif country_code_format == "8":
            prefix = "8"
        elif country_code_format is None:
            prefix = ""
        else:
            raise ValueError("Недопустимый формат кода страны. Допустимые значения: '+7', '7', '8', 'None'")

        # Форматируем номер в удобный вид: (XXX) XXX-XX-XX
        formatted_number = re.sub(
            re_sub_pattern,
            re_sub_repl,
            digits
        )

        return f"{prefix}{formatted_number}"

    def __validate_data(
        self,
        response: requests.Response,
        model_response_data=None,
        get_file: bool = False,
    ) -> Any:
        if self.__debug:
            try:
                self.logger.debug(
                    f"Входные данные:\n{response.request.url=}\n{response.request.body=}\n{response.request.headers=}\n\nВыходные данные:\n{response.headers=}\n{response.content=}\n\n")
            except Exception as err:
                self.logger.debug(f"{err=}")
        if get_file: return response.content
        response_data: dict = json.loads(response.content)

        if self.__return_dict:
            return response_data
        if model_response_data is not None:
            return model_response_data.parse_obj(response_data)
        return response_data

    def _send_request(
        self,
        url: str,
        data: dict | None = None,
        method: RequestMethod = RequestMethod.GET,
        model_response_data=None,
        get_file: bool = False,
    ) -> Any:
        self.logger.info(f"{method=}, {url=}, {data=}, {model_response_data=},")
        match method:
            case self.RequestMethod.GET:
                response = self.session_s.get(f'{self.base_url}{url}', headers=self.headers)
            case self.RequestMethod.POST:
                assert data is not None, f"При {method=} запросе, data не может быть None"
                response = self.session_s.post(f'{self.base_url}{url}', data=json.dumps(data), headers=self.headers)
            case _:
                raise ValueError(f"Method {method} not supported")

        return self.__validate_data(response, model_response_data, get_file)


class FlashCallsAPI(BaseAPI):
    def get_code(self, phone: str, sms: bool = False, ) -> GetCodeModel:
        """
        :param phone: Номер вызываемого абонента. Ограничение на количество отправок в сутки по умолчанию 3
        :param sms:Если установлено значение true, клиенту совершается звонок. Если звонок не проходит и оператор возвращает код ошибки, на номер клиента автоматически отправляется SMS с кодом авторизации. По умолчанию установлено значение false
        
        :return:
        """
        phone = self._validate_phone_number(phone, country_code_format="8", re_sub_repl=r'\1\2\3\4')
        this_url = f"/authcalls/{self.token}/get_code/{phone}"
        if sms:
            this_url = this_url + "?sms=true"
        try:

            return self._send_request(
                url=this_url,
                model_response_data=GetCodeModel,

            )
        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.get_code.__name__,
                                 f"Не удалось получить код авторизации: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.get_code.__name__,
                            f"Не удалось получить код авторизации: \n{err}")


class SMSCodeAPI(BaseAPI):
    def get_sms_code(self, phone: str, code: str | None = None,
                     ) -> GetSMSCodeModel:
        """
        Отправка кода авторизации через смс. Генерируется случайный четырех значный код. Если нужно отправить свой код,
        необходимо его передать в параметре code. Время отображения кода в Telegram чате 90 секунд.

        :param phone: Номер телефона вызываемого абонента.  Ограничение на количество отправок в сутки (опционально).
        :param code:Код авторизации, если указан отправляется данный код. Длина кода не должна превышать 4 символа.
        
        :return:
        """
        phone = self._validate_phone_number(phone, country_code_format="8", re_sub_repl=r'\1\2\3\4')

        this_url = f"/authcalls/{self.token}/get_sms_code/{phone}"
        if code is not None:
            this_url = this_url + "&code=true"
        try:

            return self._send_request(
                url=this_url,
                model_response_data=GetSMSCodeModel,
            )
        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.get_sms_code.__name__,
                                 f"Не удалось получить код авторизации: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.get_sms_code.__name__,
                            f"Не удалось получить код авторизации: \n{err}")


class TGCodeAPI(BaseAPI):
    def get_tg_code(self, phone: str, code: str | None = None,
                    ) -> GetTGCodeModel:
        """
        :param phone: Номер телефона вызываемого абонента.  Ограничение на количество отправок в сутки (опционально).
        :param code:Код авторизации, если указан отправляется данный код. Длина кода не должна превышать 4 символа.
        
        :return:
        """
        phone = self._validate_phone_number(phone, country_code_format="8", re_sub_repl=r'\1\2\3\4')
        this_url = f"/authcalls/{self.token}/get_tg_code/{phone}"

        if code is not None:
            assert len(code) == 4, "размер code не должен быть больше или меньше 4 символов"
            this_url = this_url + "&code=true"
        try:
            return self._send_request(
                url=this_url,
                model_response_data=GetTGCodeModel,

            )
        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.get_tg_code.__name__,
                                 f"Не удалось получить код авторизации: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.get_tg_code.__name__,
                            f"Не удалось получить код авторизации: \n{err}")


class BackCallsAPI(BaseAPI):
    """
    Авторизация происходит за счет звонка абонентом на случайный выделенный номер, при звонке происходит сброс вызова.
    Номер пользователя возвращается по webhook или через get запрос.
    """

    def reverse_auth_phone_get(self, phone: str, ) -> ReverseAuthPhoneGetModel:
        """
        При запросе вы получаете случайный номер для звонка, а также id для получения информации о совершении звонка абонентом на этот номер. Для получения информации используйте функцию check_phone. Время жизни номера для авторизации составляет 120 секунд.

        :param phone: Номер телефона пользователя в формате 89ххххххххх
        
        :return:
        """
        phone = self._validate_phone_number(phone, country_code_format="8", re_sub_repl=r'\1\2\3\4')

        this_url = f"/authcalls/{self.token}/reverse_auth_phone_get?phone={phone}"

        try:

            return self._send_request(
                url=this_url,
                model_response_data=ReverseAuthPhoneGetModel,

            )
        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.reverse_auth_phone_get.__name__,
                                 f"Не удалось получить случайный номер для звонка: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.reverse_auth_phone_get.__name__,
                            f"Не удалось получить случайный номер для звонка: \n{err}")

    def reverse_auth_phone_post(self, phone: str, webhook: str, ) -> ReverseAuthPhonePostModel:
        """
        При запросе вы получаете случайный номер для звонка, а также id для получения информации о совершении звонка
        абонентом на этот номер. При подтверждении авторизации отправляется webhook на указанный url.
        Время жизни номера для авторизации составляет 120 секунд.

        Формат возвращаемого webhook: url_адрес?success=True&phone=89000000000&id=000000

        :param phone: Номер телефона пользователя в формате 89ххххххххх
        :param webhook: URL для получения ответа
        
        :return:
        """
        phone = self._validate_phone_number(phone, country_code_format="8", re_sub_repl=r'\1\2\3\4')

        this_url = f"/authcalls/{self.token}/reverse_auth_phone_post"
        data = {
            "phone": phone,
            "webhook": webhook,
        }
        try:

            return self._send_request(
                url=this_url,
                data=data,
                method=self.RequestMethod.POST,
                model_response_data=ReverseAuthPhonePostModel,

            )
        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.reverse_auth_phone_post.__name__,
                                 f"Не удалось получить случайный номер для звонка: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.reverse_auth_phone_post.__name__,
                            f"Не удалось получить случайный номер для звонка: \n{err}")

    def reverse_auth_phone_check(self, id_auth: int, ) -> ReverseAuthPhoneCheckModel:
        """
        Получение номера телефона клиента по id авторизации
        :param id_auth: Id авторизации полученный от функции get_auth_phone
        
        :return:
        """

        this_url = f"/authcalls/{self.token}/reverse_auth_phone_check/{id_auth}"

        try:

            return self._send_request(
                url=this_url,
                model_response_data=ReverseAuthPhoneCheckModel,

            )
        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.reverse_auth_phone_check.__name__,
                                 f"Не удалось получить номер телефона клиента: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.reverse_auth_phone_check.__name__,
                            f"Не удалось получить номер телефона клиента: \n{err}")


class WhatsAppSMSAPI(BaseAPI):
    pass


class SettingAPI(BaseAPI):
    def get_status(self, id_status: int, ) -> GetStatusModel:
        """
        Получение информации об авторизации
        :param id_status: Идентификатор запроса (берется из get_code)
        
        :return:
        """
        this_url = f"/authcalls/{self.token}/get_status/{id_status}"
        try:

            return self._send_request(
                url=this_url,
                model_response_data=GetStatusModel,

            )
        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.get_status.__name__,
                                 f"Не удалось получить информации об авторизации: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.get_status.__name__,
                            f"Не удалось получить информации об авторизации: \n{err}")

    def get_balance(self, ) -> GetBalanceModel:
        """
        Получение остатка средств на счете
        
        :return:
        """
        this_url = f"/authcalls/{self.token}/get_balance/"
        try:

            return self._send_request(
                url=this_url,
                model_response_data=GetBalanceModel,

            )
        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.get_status.__name__,
                                 f"Не удалось получить остатки средств на счете: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.get_status.__name__,
                            f"Не удалось получить остатки средств на счете: \n{err}")

    def get_billing_record(self, count_record: int, ) -> GetBillingModel:
        """
        Получение N последних записей транзакций
        :param count_record: Количество последних записей (не больше 100)
        
        :return:
        """
        this_url = f"/authcalls/{self.token}/get_billing_record/{count_record}/"
        try:

            return self._send_request(
                url=this_url,
                model_response_data=GetBillingModel,

            )
        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.get_status.__name__,
                                 f"Не удалось получить {count_record} последних записей транзакций: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.get_status.__name__,
                            f"Не удалось получить {count_record} последних записей транзакций: \n{err}")

    def get_billing_csv(
        self,
        start_date: datetime.datetime | str,
        path_save_file: pathlib.Path | str,
        file_name: str = "billing.csv",

    ):
        """
        Получение экспорта данных записей транзакций в csv формате

        :param path_save_file: Путь для сохранения файла, если директорий не существует они будут созданы
        :param file_name: имя файла с указанным форматом .csv, но если не указано, то мы укажем =), стандартное имя billing.csv
        :param start_date: Дата начала выгрузки формата YYYY-MM-DD
        
        """
        if isinstance(start_date, datetime.datetime):
            start_date = start_date.strftime('%Y-%m-%d')
        elif isinstance(start_date, str):
            try:
                datetime.datetime.strptime(start_date, "%m/%d/%Y")
            except ValueError:
                raise ValueError("Incorrect data format, should be YYYY-MM-DD")
        this_url = f"/authcalls/{self.token}/get_billing_csv/{start_date}/"
        try:
            # Убедимся, что путь корректный для любой ОС
            path_save_file = os.path.normpath(path_save_file)

            # Создаём директорию, если её нет
            os.makedirs(path_save_file, exist_ok=True)

            # Добавляем расширение .csv, если его нет
            if not file_name.lower().endswith('.csv'):
                file_name += '.csv'

            # Полный путь к файлу
            full_path = os.path.join(path_save_file, file_name)
            data_file = self._send_request(
                url=this_url,
                get_file=True,

            )
            with open(full_path, 'wb') as file:
                file.write(data_file)

        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.get_billing_csv.__name__,
                                 f"Не удалось получить экспорт данных записей транзакций в csv формате: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.get_billing_csv.__name__,
                            f"Не удалось получить экспорт данных записей транзакций в csv формате: \n{err}")

    def post_billing_data(
        self,
        start_date: datetime.datetime | str,
        end_date: datetime.datetime | str,
    ) -> GetBillingModel:
        """
        Получение записей транзакций

        :param start_date: Дата начала получения данных формата YYYY-MM-DD
        :param end_date: Дата конца получения данных формата YYYY-MM-DD
        
        :return:
        """
        data = {
            'start_date': start_date,
            'end_date': end_date
        }
        if isinstance(start_date, datetime.datetime):
            data['start_date'] = start_date.strftime('%Y-%m-%d')
        elif isinstance(start_date, str):
            try:
                datetime.datetime.strptime(start_date, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Incorrect data format, should be YYYY-MM-DD")
        if isinstance(end_date, datetime.datetime):
            data['end_date'] = end_date.strftime('%Y-%m-%d')
        elif isinstance(end_date, str):
            try:
                datetime.datetime.strptime(end_date, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Incorrect data format, should be YYYY-MM-DD")

        this_url = f"/authcalls/{self.token}/post_billing_data/"

        try:
            return self._send_request(
                url=this_url,
                data=data,
                method=self.RequestMethod.POST,
                model_response_data=GetBillingModel,

            )
        except requests.exceptions.RequestException as err:
            raise TokenException(self.__class__.__qualname__,
                                 self.post_billing_data.__name__,
                                 f"Не удалось получить записи транзакций: \n{err}")
        except TypeError as err:
            raise TypeError(self.__class__.__qualname__,
                            self.post_billing_data.__name__,
                            f"Не удалось получить записи транзакций: \n{err}")


class TelefonIpAPI(FlashCallsAPI, BackCallsAPI, SMSCodeAPI, TGCodeAPI, WhatsAppSMSAPI, SettingAPI):
    pass
