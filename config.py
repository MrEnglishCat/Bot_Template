# Файл с конфигурационными данными для бота, базы данных, сторонних сервисов и т.п.
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pprint import pprint

from aiogram.utils import markdown
from environs import Env

from Bot.utils.utils import get_full_path_logger, Files, escape_md, get_random_wishes

logger = logging.getLogger(f"__main__.{__name__}")
logger.setLevel(logging.DEBUG)

file_formatter = logging.Formatter(
    '[{asctime}] #{levelname:8} {filename}::{lineno}::{funcName} ===> {name} ===> {message}',
    style="{",
    datefmt="%d-%m-%Y %H:%M:%S"
)
file_handler = RotatingFileHandler(
    get_full_path_logger(logger.name, __name__, logger.level),
    maxBytes=5 * 1024 * 1024,
    backupCount=5,
    encoding="utf-8",
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


@dataclass
class DatabaseConfig:
    database: str = None
    db_host: str = None
    db_user: str = None
    db_password: str = None


@dataclass
class RePatterns:
    # Регулярное выражение для определения URL
    pattern_telegram_username = re.compile(r"(?<=@)[\w.\-]+")
    pattern_telegram_url = re.compile(r"(?<=https://t\.me/)[\w.\-]+")
    # user_status = lambda self, status: re.compile(fr"(?<=/{status})\w+") --- если команду определять в момент обращения к user_status
    add_user_status = re.compile(fr"(?<=/add)\w+")
    delete_user_status = re.compile(fr"(?<=/delete)\w+")
    salt = 'ARES_resumeBot'  # TODO сделать рандомизацию соли


    def get_userstatus(self, status):
        return re.compile(fr"(?<=/{status})\w+")


@dataclass
class FilePath:
    env_path: str = f"Bot/config_data/.env"
    base: str = f"Bot/botDataFiles"
    base_path: str = f'Bot/botDataFiles/UsersData'
    info_path: str = f'info'
    ids_path: str = f'ids'
    result_path: str = f'result'
    new_auth_ids_path: str = f'new_auth_users'
    json_path: str = f'json'
    logs = 'logging'
    image_path: str = 'images'
    loggerDRIVER: str = "Bot/botDataFiles/logging/loggerDRIVER.txt"
    zipfile_path: str = f'Bot/botDataFiles/[{datetime.now().strftime("%d_%m_%Y %H.%M")}]_zipfille_path.zip'

    for_creating = (
        f"{base_path}/{info_path}",
        f"{base_path}/{ids_path}",
        f"{base_path}/{new_auth_ids_path}",
    )

    supervisors_info: str = f'{base_path}/{info_path}/supervisors_info.json'
    admins_info: str = f'{base_path}/{info_path}/admins_info.json'
    users_info: str = f'{base_path}/{info_path}/users_info.json'
    other_users_info: str = f'{base_path}/{info_path}/other_users_info.json'  # Хранит пользователей, которые нажимали
    # когда-либо кнопку старт, не вошедшие
    #  в supervisors_info,admins_info,users_info

    supervisor_ids: str = f'{base_path}/{ids_path}/supervisors_ids.json'
    admin_ids: str = f'{base_path}/{ids_path}/admins_ids.json'
    user_ids: str = f'{base_path}/{ids_path}/users_ids.json'

    new_auth_users: str = f'{base_path}/{new_auth_ids_path}/new_auth_users.json'
    images: str = f"Bot/config_data/{image_path}/no_username.mp4"

    service_commands = {
        "getLogs": f"{base}/{logs}",
        "getAllResultJSONZip": f"{base}/{result_path}/{json_path}",
        "getLastJSONTest": f'{base}/{result_path}/test/one/test.json',
        "getAllJSONTestZip": f'{base}/{result_path}/test/total',
        "getNewUsers": new_auth_users,
        "getAllUsers": users_info,
        "getAllAdmins": admins_info,
        "getAllSupervisors": supervisors_info,
        "getOtherUsers": other_users_info,
        "getALL": f'{base_path}/{info_path}',
        "clearAllNewAuthUsers": new_auth_users,
        "deleteSupervisors": supervisor_ids,
        "deleteAdmins": admin_ids,
        "deleteUsers": user_ids,
    }


@dataclass
class Texts:
    SUPERVISOR = "supervisor"
    ADMIN = "admin"
    USER = "user"
    # TODO сделать все через словари
    start = {

        "auth": (
            '🔗 Отправьте мне ссылку  на резюме что бы освободить себе немного времени 🙂. 🔗',
            # escape_md(get_random_wishes()),)
        ),
        "other": get_random_wishes,
    }

    help = {
        "supervisor": (
            r'🆘 /help что бы показать описание команд;',
            fr'🆘 /helpDEBUG что бы показать описание команд {markdown.bold("ОТЛАДКИ")};',
            r'⏬ /addSupervisors добавить пользователя(-ей) со статусом Supervisor;',
            r'⏬ /addAdmins добавить пользователя(-ей) со статусом Admin;',
            r'⏬ /addUsers добавить пользователя(-ей) со статусом User;',
            f'🗑 /delete(Supervisors, Admins, Users) для удаления юзеров [{markdown.bold("в РАЗРАБОТКЕ")}];\n',
            f'⚠️️ Формат команд /add & /delete: \n \t\t"/addAdmins {markdown.bold(r"https://t.me/Username")}";\n\t\t"/addAdmins {markdown.bold(r"@Username")}";\n\t\t"/deleteAdmins {markdown.bold(r"https://t.me/Username")}";\n\t\t"/deleteAdmins {markdown.bold(r"@Username")}".',
            f"ℹ️ Пока что бот нужен только для обработки ссылок.",

            f'⚠️ Для запуска обработки резюме нужно отправить боту в сообщении {markdown.italic("ТОЛЬКО")} ссылку на резюме;',

            f'➡️ Ссылка обязательно должна начинаться на {markdown.bold("https://")}, {markdown.bold("http://")}',
            f"⛔️ Произвольный текст в сообщении с сылкой не приветствуется!",
        ),
        "admin": (
            r'🆘 /help что бы показать описание команд;',
            r'⏬ /addAdmins добавить пользователя(-ей) со статусом Admin;',
            r'⏬ /addUsers добавить пользователя(-ей) со статусом User;',
            f'🗑 /delete(Admins, Users) для удаления юзеров [{markdown.bold("в РАЗРАБОТКЕ")}];\n',
            f'⚠️️ Формат команд /add & /delete: \n \t\t"/addAdmins {markdown.bold(r"https://t.me/Username")}";\n\t\t"/addAdmins {markdown.bold(r"@Username")}";\n\t\t"/deleteAdmins {markdown.bold(r"https://t.me/Username")}";\n\t\t"/deleteAdmins {markdown.bold(r"@Username")}".',
            f'⚠️ Для запуска обработки резюме нужно отправить боту в сообщении {markdown.italic("ТОЛЬКО")} ссылку на резюме;',
            f'➡️ Ссылка обязательно должна начинаться на {markdown.bold("https://")}, {markdown.bold("http://")}',
            f"⛔️ Произвольный текст в сообщении с сылкой не приветствуется!",
        ),
        "user": (
            r'🆘 /help что бы показать описание команд;',
            f'⚠️ Для запуска обработки резюме нужно отправить боту в сообщении {markdown.italic("ТОЛЬКО")} ссылку на резюме;',
            f'➡️ Ссылка обязательно должна начинаться на {markdown.bold("https://")}, {markdown.bold("http://")}',
            f"⛔️ Произвольный текст в сообщении с сылкой не приветствуется!",
        ),
        "other": (
            r'☄️ /start для запуска бота. Получение приветственного сообщения;',
            r'🆘 /help что бы показать описание команд;',
        ),
        "helpDEBUG": (
            fr'❤️‍🩹 Команды ниже для {markdown.bold("ОТЛАДКИ")} ❤️‍🩹',
            fr'🔧 /getLogs для получения архива с логами;',
            fr'🔧 /getAllResultJSONZip для получения архива с результатами в JSON;',
            f'🔧 /getLastJSONTest для получения файла JSON с исходными данными последней анкеты;',
            f'🔧 /getAllJSONTestZip для получение всех файлов JSON с исходными данными анкет;',
            f'🔧 /getAllUsers для получения файла JSON сданными Users;',
            f'🔧 /getAllAdmins для получения файла JSON сданными Admins;',
            f'🔧 /getAllSupervisors для получения файла JSON  сданными Supervisors;',
            f'🔧 /getALL для получения всех файлов с информацией о пользователях;',
            f'🔧 /getNewUsers для получения добавленных пользователей, которые еще не прошли авторизацию;',
            f'🔧 /deleteNewAuthUsers для удаления новых ошибочно добавленных пользователей (которые не прошли еще авторизацию) [{markdown.bold("в РАЗРАБОТКЕ")}];',
            f'🔧 /clearAllNewAuthUsers для ⚠️ {markdown.bold("удаления файла")} ⚠️ JSON с новыми пользователями ️ ⚠️{markdown.bold("БЕЗ НАДОБНОСТИ НЕ ТРОГАТЬ")}⚠️;\n',
        )
    }

    echo = {
        "auth": (
            '🔗 Вы авторизованы, вы можете работать с ботом! 🔗',
            f"⛔️ Произвольный текст в сообщении со сылкой не приветствуется!",
            f"💬 {get_random_wishes()}"
        ),
        "other": (
            '💪 Да прибудет с тобой сила! 💪',
            '⛔️ Работа производится только с авторизованными пользователями ⛔️',
            f"💬 {get_random_wishes()}"
        )
    }

    add_admin_auth = (
        # escape_md('🏁 Добавление пользователей прошло успешно! 🏁'),
        escape_md('Далее добавленным пользователям нужно пройти авторизацию по сформированной инструкции ниже.'),
    )
    add_admin_error = f'В переданных данных не получилось распознать ссылку вида: \n\n "{markdown.bold(r"https://t.me/<Username>")}";\n"{markdown.bold(r"@<Username>")}"'

    instructions_for_new_user = (
        escape_md(
            f"Для прохождения авторизации и получения прав доступа. \nПерейдите по ссылке: https://t.me/ARES_resumeBot.\nДалее нужно нажать кнопку START для того что бы пройти авторизацию.\nПосле можете воспользоваться командой /help для получения списка доступных команд."),
    )

    hh_wait_message = escape_md("⏳ Опускается занавес, начинается магия...🔮")
    hh_error_message = r"🚫 Что\-то пошло не так, орбратитесь за помощью к Магам\. 🔮",
    hh_success_message = (escape_md("🪄 Магия свершилась! ✨"),
                          escape_md("📄 Ваш запрошенный файл 📄"),
                          escape_md(f"📄 {get_random_wishes()} 📄"),
                          )

    success_auth = escape_md(f'Поздравляю, добрый путник!\nАвторизация пройдена успешно!')


@dataclass
class Commands:
    """
    Возможно понадобится для использования в фильтрах
    """
    general: tuple = ('start', 'help')
    admins: tuple = ('addAdmins', 'addUsers', 'deleteAdmins',
                     'deleteUsers')  # Не весь список команд. Используется для фильтров указанных команд
    users: tuple = ('',)  # Не весь список команд. Используется для фильтров указанных команд
    supervisors: tuple = (
        'addSupervisors', 'addAdmins', 'addUsers',
        'deleteAdmins', 'deleteUsers', 'deleteSupervisors',
        'getLogs', 'getLastJSONTest', 'getAllJSONTestZip', 'getAllUsers',
        'getAllAdmins', 'getAllSupervisors', 'getALL', 'getNewUsers', 'clearAllNewAuthUsers'
    )  # Не весь список команд. Используется для фильтров указанных команд


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту
    supervisor_ids: set[int]  # Список id супревайзерами бота
    admin_ids: set[int]  # Список id администраторов бота
    user_ids: set[int]  # Список id пользователями бота
    statuses: tuple[str] = ("supervisor", "admin", "user")
    texts: Texts = field(default_factory=Texts)
    commands: Commands = field(default_factory=Commands)

    def get_user_status(self, user_id: int, is_check_ids: bool = True, return_only_status: bool = False) -> str:
        """
        По полученному от ТГ id определяет статус юзера и
        выдает определенный путь для сохранения файлов либо "..._info.json", либо "..._ids.json"
        :param is_check_ids: если True то вернет пути для "..._ids.json" иначе для "..._info.json"
        :param return_only_status: если True то будет возвращен только статуст юзера
        :param user_id: идентификатор пользователя
        :return:
        """
        if return_only_status:
            logger.info(f"Получение статуса пользователя...")
        else:
            logger.info(f"Получение пути к файлу для сохранении данных о пользователе...")
        statuses: list[dict] = [
            {
                "status": "supervisor",
                "path": FilePath.supervisor_ids if is_check_ids else FilePath.supervisors_info,
                "ids": self.supervisor_ids
            },
            {
                "status": "admin",
                "path": FilePath.admin_ids if is_check_ids else FilePath.admins_info,
                "ids": self.admin_ids
            },
            {
                "status": "user",
                "path": FilePath.user_ids if is_check_ids else FilePath.users_info,
                "ids": self.user_ids
            }
        ]

        for data in statuses:
            if user_id in data.get("ids"):
                if return_only_status:
                    return data.get("status")
                return data.get("path")

    def update_supervisor_ids(self, ids: list[int]) -> None:
        """
        Метод для добавления ids к supervisor_ids
        :param ids:
        :return:
        """
        self.supervisor_ids.update(ids)

    def update_admin_ids(self, ids: list[int]) -> None:
        """
        Метод для добавления ids к admin_ids
        :param ids:
        :return:
        """
        self.admin_ids.update(ids)

    def update_users_ids(self, ids: list[int]) -> None:
        """
        Метод для добавления ids к users_ids
        :param ids:
        :return:
        """
        self.user_ids.update(ids)

    def update_ids(self) -> None:
        supervisor_ids = Files.read_json(FilePath.supervisor_ids)
        admin_ids = Files.read_json(FilePath.admin_ids)
        user_ids = Files.read_json(FilePath.user_ids)

        if supervisor_ids:
            self.update_supervisor_ids(supervisor_ids.values())
            logger.info(f"IDs Supervisors загружены из файла!")

        if admin_ids:
            self.update_admin_ids(admin_ids.values())
            logger.info(f"IDs Админов загружены из файла!")

        if user_ids:
            self.update_users_ids(user_ids.values())
            logger.info(f"IDs авторизованных Пользователей загружены из файла!")

    def add_admin(self):
        ...


@dataclass
class HHService:
    hh_username: str
    hh_password: str


@dataclass
class Config:
    tg_bot: TgBot
    hh: HHService
    patterns: RePatterns = field(default_factory=RePatterns)
    filepath: FilePath = field(default_factory=FilePath)
    db: DatabaseConfig = field(default_factory=DatabaseConfig, init=False)


def load_config(env_path) -> Config:
    env: Env = Env()
    env.read_env(env_path)
    logger.info("Чтение файла с переменными окружения завершено.")
    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_ids=set(map(int, filter(bool, env.list('ADMIN_IDS')))),
            user_ids=set(map(int, filter(bool, env.list('USER_IDS')))),
            supervisor_ids=set(map(int, filter(bool, env.list('SUPERVISOR_IDS')))),
        ),
        hh=HHService(
            hh_username=env('HH_USERNAME'),
            hh_password=env('HH_PASSWORD'),
        )
        # db=DatabaseConfig(
        #     database=env('DATABASE'),
        #     db_host=env('DB_HOST'),
        #     db_user=env('DB_USER'),
        #     db_password=env('DB_PASSWORD')
        # )
    )
