import logging
import sys
from logging.handlers import TimedRotatingFileHandler

FORMATTER = logging.Formatter(
    "%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
LOG_FILE = "secondRoomBotDebug3.log"


def get_console_handler():
    consoleHandler = logging.StreamHandler(sys.stderr)
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
ClientLogger = get_logger('Client')
AdminLogger = get_logger('Administration')
InitLogger = get_logger("Initialization")
