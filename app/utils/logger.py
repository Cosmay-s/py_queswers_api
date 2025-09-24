from loguru import logger
import sys
import os


log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)


logger.remove()


logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> |"
    "<level>{level: <8}</level> |"
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> -"
    "<level>{message}</level>",
    level="INFO",
    colorize=True
)


logger.add(
    f"{log_dir}/app.log",
    rotation="10 MB",
    retention="10 days",
    format="{time:YYYY-MM-DD HH:mm:ss} |"
    "{level: <8} | {name}:{function}:{line} - {message}",
    level="DEBUG"
)


def get_logger():
    return logger
