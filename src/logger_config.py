from config import Config
from loguru import logger

logger.add(Config.LOG_FILE, rotation="1 MB")


def get_logger():
    return logger
