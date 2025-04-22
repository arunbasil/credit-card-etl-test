import os
import logging


def get_logger(name):
    log_dir = "test/logs"
    os.makedirs(log_dir, exist_ok=True)  # Ensure directory exists

    log_file = os.path.join(log_dir, "test.log")

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(file_handler)

    return logger
