import logging

def get_logger(name=__name__):
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
        )

        # Console handler
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        # Optional: Uncomment to log to file as well
        file_handler = logging.FileHandler("logs/test.log")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        logger.propagate = False  # Prevent duplicate logs in pytest

    return logger
