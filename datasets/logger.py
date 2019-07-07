import logging

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


def init(name, log_file, level=logging.INFO):
    """Function setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

APP_LOGGER = init('app','app.log')