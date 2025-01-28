import asyncio
import logging
from logging.handlers import RotatingFileHandler

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from Bot.config_data.config import Config, load_config
from Bot.filters.default import HaveUsername
from Bot.handlers import other_handlers, auth, other

# Markdown-теги:
#
# *текст* — Жирный.
# _текст_ — Курсив.
# __текст__ — Подчеркнутый.
# ~текст~ — Зачеркнутый.
# [Текст](URL) — Гиперссылка.

# MARKDOWN_V_2:
# text = (
#         "*Жирный текст*\\n"
#         "_Курсивный текст_\\n"
#         "\\[Экранированная квадратная скобка\\]\\n"
#         "[Ссылка на Google](https://www.google.com)"
#     )


# Импортируем роутеры
# ...
# Импортируем миддлвари
# ...
# Импортируем вспомогательные функции для создания нужных объектов
# ...
from Bot.keyboards.main_menu import set_main_menu
from Bot.utils.statistics import UserInfo
from Bot.utils.utils import get_full_path_logger, Files

# Инициализируем логгер
# В библиотеке logging уже реализовано довольно много полезных хэндлеров для управления
# логами: логи можно отправлять по электронной почте SMTPHandler, "из коробки" можно создать
# ротацию файлов с логами, при достижении ими определенного объема или по времени - RotatingFileHandler
# и TimedRotatingFileHandler, можно отправлять логи по HTTP - HTTPHandler и так далее. Список других
# полезных готовых хэндлеров можно посмотреть здесь. А если вам не хватит готовых хэндлеров - всегда
# можно написать свой, отнаследовавшись от класса Handler библиотеки logging.
# Порядок следования приоритетов уровней логов. Если DEBUG - выводятся все.
# logger.debug('Это лог уровня DEBUG')
# logger.info('Это лог уровня INFO')
# logger.warning('Это лог уровня WARNING')
# logger.error('Это лог уровня ERROR')
# logger.critical('Это лог уровня CRITICAL')

logger = logging.getLogger(__name__)

async def main() -> None:
    """
    Функция конфигурирования и запуска бота
    :return:
    """
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
    logger.addHandler(logging.StreamHandler())  # убрать при деплое
    logger.info('Start logging.')

    # logger.addFilter()


    # Загружаем конфиг в переменную config
    config: Config = load_config("Bot/config_data/.env")
    # Создание каталогов
    logger.info(f"Создание необходимых директорий для работы скрипта...")
    for folder in config.filepath.for_creating:
        Files.checking_folder(folder)

    logger.info("Старт загрузки данных сохранённых ID авторизованных пользователей.")
    config.tg_bot.update_ids()
    logger.info("Завершнна загрузка данных сохранённых ID авторизованных пользователей.")




    # Инициализируем бот и диспетчер
    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2)
    )
    dp = Dispatcher()
    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting Bot.')

    # Инициализируем объект хранилища
    storage = ...

    # Инициализируем другие объекты (пул соединений с БД, кеш и т.п.)
    # ...


    # Помещаем нужные объекты в workflow_data диспетчера
    dp.workflow_data.update(
        {
            'config': config,
            'UserInfo': UserInfo()
        }
    )
    # Настраиваем главное меню бота
    # await set_main_menu(bot)

    logger.info('Подключаем Routers.')
    main_router = Router()
    main_router.message.filter(HaveUsername())
    main_router.include_routers(
        auth.router_auth,  # комманды и др хэндлеры для авторизованных пользователей
        other.router_other,  # команды для неавторизованных пользователей
        other_handlers.router,  # echo_reply
    )
    dp.include_router(
        main_router
    )

    # Регистрируем миддлвари
    logger.info('Подключаем Middleware.')
    # ...

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)



if __name__ == '__main__':
    asyncio.run(
        main()
    )
