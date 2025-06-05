from abc import ABC, abstractmethod
from typing import Generic, TypeVar

TEntity = TypeVar("TEntity")


class BaseModel(
    Generic[TEntity],
    ABC,
):
    @classmethod
    @abstractmethod
    def get_columns(cls) -> list[str]: ...

    @abstractmethod
    def to_entity(self) -> TEntity: ...

    @classmethod
    @abstractmethod
    def from_entity(cls, entity: TEntity) -> "BaseModel": ...

    @classmethod
    @abstractmethod
    def from_row_to_entity(cls, row: dict) -> TEntity: ...

    @abstractmethod
    def to_dict(self) -> dict: ...
