import logging
import sys
from logging.handlers import TimedRotatingFileHandler

FORMATTER = logging.Formatter(
    "%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
LOG_FILE = "secondRoomBot.log"


def get_console_handler():
    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(FORMATTER)
    return consoleHandler


def get_file_handler():
    fileHandler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
    fileHandler.setFormatter(FORMATTER)
    return fileHandler


def get_logger(logger_name: str):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    logger.propagate = False
    return logger


DBLogger = get_logger('Database')
AdminLogger = get_logger('Administration')
InitLogger = get_logger("Initialization")
