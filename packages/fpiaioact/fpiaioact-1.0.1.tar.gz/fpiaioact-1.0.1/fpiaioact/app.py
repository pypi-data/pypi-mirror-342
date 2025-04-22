from __future__ import annotations
import typing as t
from asyncio import BaseEventLoop, get_event_loop, run
from .runners import ActorSystem


class ActorApp:
    """
    Класс для управления системой акторов.
    """
    _name: str
    _map: t.Dict[str, t.Callable] = {}

    def __init__(self, name: str, *, loop: BaseEventLoop | None = None):
        self._name = name
        self._loop = loop if loop else get_event_loop()

    def __call__(self, name: str) -> t.Callable:
        """
        Возвращает актора по его имени.
        """
        if name not in self._map:
            raise ValueError(f"Актор с именем '{name}' не зарегистрирован.")
        return self._map[name]

    def register(self, tasks: dict[str, t.Callable], cleanup: bool = False) -> ActorApp:
        """
        Регистрирует акторы в системе.
        """
        if cleanup:
            self._map.clear()
        self._map.update(tasks)
        return self

    def start_actor(self, name: str):
        """
        Синхронный запуск актора.
        """
        actor_callable = self(name)
        actor_system = ActorSystem(loop=self._loop)
        # Здесь вызываем корутину actor_callable как синхронную задачу
        run(actor_callable(actor_system))

    async def run_actor(self, name: str):
        """
        Асинхронный запуск актора.
        """
        actor_callable = self(name)
        actor_system = ActorSystem(loop=self._loop)
        await actor_callable(actor_system).run_all()

    async def run_actors(self, *names: str):
        """
        Асинхронный запуск нескольких акторов по их именам.
        """
        system = ActorSystem(loop=self._loop)

        for name in names:
            actor_callable = self(name)
            system.add(name, actor_callable)

        await system.run_all()

    @property
    def name(self) -> str:
        return self._name
