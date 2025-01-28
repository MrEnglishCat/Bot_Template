# Файл с конфигурационными данными для бота, базы данных, сторонних сервисов и т.п.
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(f"__main__.{__name__}")
logger.setLevel(logging.DEBUG)

file_formatter = logging.Formatter(
    '[{asctime}] #{levelname:8} {filename}::{lineno}::{funcName} ===> {name} ===> {message}',
    style="{",
    datefmt="%d-%m-%Y %H:%M:%S"
)
file_handler = RotatingFileHandler(
    filename="/tmp/bot.log",
    maxBytes=5 * 1024 * 1024,
    backupCount=5,
    encoding="utf-8",
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)