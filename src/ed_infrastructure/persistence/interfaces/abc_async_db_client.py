from abc import ABCMeta, abstractmethod


class ABCAsyncDbClient(metaclass=ABCMeta):
    @abstractmethod
    async def start(self): ...

    @abstractmethod
    async def stop(self): ...
