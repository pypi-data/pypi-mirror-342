import asyncio
from logging import getLogger

class ActorSystem:
    """
    Система акторов для управления и выполнения задач.
    """
    def __init__(self, *, loop=None):
        self.logger = getLogger("ActorSystem")
        self.tasks = []
        self.actor_map = {}
        self.loop = loop or asyncio.get_event_loop()

    def add(self, name: str, actor):
        """
        Добавляет актор в систему.
        """
        if name in self.actor_map:
            self.logger.error(f"Актор с именем '{name}' уже зарегистрирован.")
            return
        self.actor_map[name] = actor
        self.logger.info(f"Актор '{name}' добавлен в систему.")

    async def run_actor(self, name: str):
        """
        Асинхронный запуск конкретного актора.
        """
        if name not in self.actor_map:
            self.logger.error(f"Актор с именем '{name}' не найден.")
            return
        self.logger.info(f"Запуск актора '{name}'...")
        await self.actor_map[name](self)  # передаём system

    def start(self):
        """
        Синхронный запуск всех зарегистрированных задач.
        """
        self.logger.info("Запуск системы акторов...")
        asyncio.run(self._run_all())

    async def run_all(self):
        """
        Асинхронный запуск всех задач.
        """
        await self._run_all()

    async def _run_all(self):
        """
        Запуск всех зарегистрированных задач.
        """
        if not self.actor_map:
            self.logger.warning("Нет зарегистрированных акторов.")
            return
        tasks = [actor(self) for actor in self.actor_map.values()]  # передаём system
        self.logger.info(f"Запуск {len(tasks)} акторов...")
        await asyncio.gather(*tasks)
