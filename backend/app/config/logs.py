import logging


def logConfiguration():
    logging.getLogger("passlib").setLevel(logging.ERROR)
