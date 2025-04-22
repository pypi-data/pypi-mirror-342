from logging import Logger


def base_logger(logger: Logger):
    """
    Декоратор для добавления базового логгера в класс.
    """
    def setup_logger(cls):
        cls.logger = logger.getChild(cls.__name__)
        return cls

    return setup_logger
