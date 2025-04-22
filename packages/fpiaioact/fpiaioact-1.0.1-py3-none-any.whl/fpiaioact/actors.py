from logging import Logger
from abc import ABC, abstractmethod


class Actor(ABC):
    """
    Базовый класс актора. Реализует базовую структуру актора.
    """

    def __init__(self, name: str, logger: Logger | None = None):
        self.name = name
        self.logger = logger or self.get_default_logger()

    @abstractmethod
    async def __call__(self, *args, **kwargs):
        """
        Метод, который должен быть реализован в подклассах.
        """
        raise NotImplementedError

    def get_default_logger(self) -> Logger:
        from logging import getLogger
        return getLogger(self.name)
