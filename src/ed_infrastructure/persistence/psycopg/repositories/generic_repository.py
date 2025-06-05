from typing import Any, Generic, Type, TypeVar
from uuid import UUID

from ed_domain.persistence.async_repositories.abc_async_generic_repository import \
    ABCAsyncGenericRepository
from psycopg.rows import dict_row

from ed_infrastructure.persistence.psycopg.db_client import PsycopgDbClient
from ed_infrastructure.persistence.psycopg.models.base_model import BaseModel

TEntity = TypeVar("TEntity")
TModel = TypeVar("TModel", bound=BaseModel)


class GenericRepository(Generic[TEntity, TModel], ABCAsyncGenericRepository[TEntity]):
    def __init__(
        self, db_client: PsycopgDbClient, model_type: Type[TModel], table_name: str
    ):
        self._db_client = db_client
        self._model_type = model_type
        self._table_name = table_name

    async def get_all(self, **filters: Any) -> list[TEntity]:
        where_clause, values = self._build_where_clause(filters)
        query = f"SELECT * FROM {self._table_name} {where_clause}; "

        async with self._db_client.connection.cursor(row_factory=dict_row) as cur:
            await cur.execute(query, values)  # type: ignore
            rows = await cur.fetchall()

            return [self._model_type.from_row_to_entity(row) for row in rows]

    async def get(self, **filters: Any) -> TEntity | None:
        where_clause, values = self._build_where_clause(filters)
        query = f"SELECT * FROM {self._table_name} {where_clause} LIMIT 1;"

        async with self._db_client.connection.cursor(row_factory=dict_row) as cur:
            await cur.execute(query, values)  # type: ignore
            row = await cur.fetchone()
            return self._model_type.from_row_to_entity(row) if row else None

    async def create(self, entity: TEntity) -> TEntity:
        model_dict = self._model_type.from_entity(entity).to_dict()
        columns = self._model_type.get_columns()

        placeholders = ", ".join(columns)
        values = ", ".join(f"%({column})s" for column in columns)
        query = f"INSERT INTO {self._table_name} ({placeholders}) VALUES ({values}) RETURNING *;"

        async with self._db_client.connection.cursor(row_factory=dict_row) as cur:
            print("Query:", query)
            print(
                "Params:", {col: model_dict[col] for col in columns}
            )  # optional debug print
            await cur.execute(query, model_dict)  # type: ignore
            row = await cur.fetchone()
            return self._model_type.from_row_to_entity(row)  # type: ignore

    async def create_many(self, entities: list[TEntity]) -> list[TEntity]:
        if not entities:
            return []

        columns = self._model_type.get_columns()

        placeholders = ", ".join(columns)
        values = ", ".join(f"%({column})s" for column in columns)
        query = f"INSERT INTO {self._table_name} ({placeholders}) VALUES ({values}) RETURNING *;"

        result: list[TEntity] = []
        async with self._db_client.connection.cursor(row_factory=dict_row) as cur:
            for entity in entities:
                model_dict = self._model_type.from_entity(entity).to_dict()
                await cur.execute(query, model_dict)  # type: ignore
                row = await cur.fetchone()
                result.append(
                    self._model_type.from_row_to_entity(row),  # type: ignore
                )
        return result

    async def update(self, id: UUID, entity: TEntity) -> bool:
        fields = entity.__dict__
        set_clause = ", ".join(f"{key} = %({key})s" for key in fields)
        query = f"UPDATE {self._table_name} SET {set_clause} WHERE id = %(id)s;"
        fields["id"] = str(id)

        async with self._db_client.connection.cursor() as cur:
            await cur.execute(query, fields)  # type: ignore
            return cur.rowcount > 0

    async def delete(self, id: UUID) -> bool:
        query = f"DELETE FROM {self._table_name} WHERE id = %s;"

        async with self._db_client.connection.cursor() as cur:
            await cur.execute(query, (str(id),))  # type: ignore
            return cur.rowcount > 0

    def _build_where_clause(
        self, filters: dict[str, Any]
    ) -> tuple[str, dict[str, Any]]:
        if not filters:
            return "", {}
        clause = " AND ".join(f"{key} = %({key})s" for key in filters)
        return f"WHERE {clause}", filters
