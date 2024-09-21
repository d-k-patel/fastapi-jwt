import logging
import os
import sys
from datetime import datetime

from colorama import Fore, Style

# create the logs directory if it doesn't exist
if not os.path.exists("logs"):
    os.makedirs("logs")

# define the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create a file handler
handler = logging.FileHandler("logs/app.log")
handler.setLevel(logging.DEBUG)

# create a logging format
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# create a console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)

# add the console handler to the logger
logger.addHandler(console_handler)

# add the file handler to the logger
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

# define the colors for the log levels
colors = {
    "DEBUG": Fore.CYAN,
    "INFO": Fore.GREEN,
    "WARNING": Fore.YELLOW,
    "ERROR": Fore.RED,
    "CRITICAL": Fore.RED,
}


def log(level, message):
    """
    Log a message with a specific level.

    Args:
        level (str): The level of the log message.
        message (str): The message to be logged.
    """

    # get the current time
    now = datetime.now()

    # format the log message
    log_message = f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] {message}"

    # get the log level color
    color = colors.get(level, Fore.WHITE)

    # log the message with the specified level
    if level == "DEBUG":
        logger.debug(f"{Style.BRIGHT}{color}{log_message}{Style.RESET_ALL}")
    elif level == "INFO":
        logger.info(f"{Style.BRIGHT}{color}{log_message}{Style.RESET_ALL}")
    elif level == "WARNING":
        logger.warning(f"{Style.BRIGHT}{color}{log_message}{Style.RESET_ALL}")
    elif level == "ERROR":
        logger.error(f"{Style.BRIGHT}{color}{log_message}{Style.RESET_ALL}")
    elif level == "CRITICAL":
        logger.critical(f"{Style.BRIGHT}{color}{log_message}{Style.RESET_ALL}")
    else:
        logger.info(f"{Style.BRIGHT}{color}{log_message}{Style.RESET_ALL}")


def debug(message):
    """
    Log a debug message.

    Args:
        message (str): The message to be logged.
    """

    log("DEBUG", message)


def info(message):
    """
    Log an info message.

    Args:
        message (str): The message to be logged.
    """

    log("INFO", message)


def warning(message):
    """
    Log a warning message.

    Args:
        message (str): The message to be logged.
    """

    log("WARNING", message)


def error(message):
    """
    Log an error message.

    Args:
        message (str): The message to be logged.
    """

    log("ERROR", message)


def critical(message):
    """
    Log a critical message.

    Args:
        message (str): The message to be logged.
    """

    log("CRITICAL", message)
