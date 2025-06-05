from ed_domain.core.async_repositories.abc_async_generic_repository import \
    ABCAsyncGenericRepository
from psycopg import AsyncConnection

from src.ed_infrastructure.persistence.psycopg.repositories.generic_repository import \
    GenericRepository


class AsyncUnitOfWork:
    def __init__(self, conn_factory, repo_configs: dict[str, tuple[type, str]]):
        """
        repo_configs: dict of {attr_name: (EntityClass, table_name)}
        e.g., {
            "bill_repository": (Bill, "bills"),
            "user_repository": (User, "users"),
        }
        """
        self._conn_factory = conn_factory
        self._repo_configs = repo_configs
        self._conn: AsyncConnection | None = None
        self._repos: dict[str, ABCAsyncGenericRepository] = {}

    async def __aenter__(self):
        self._conn = await self._conn_factory()
        await self._conn.execute("BEGIN")

        for attr_name, (entity_cls, table_name) in self._repo_configs.items():
            repo = GenericRepository(self._conn, table_name, entity_cls)
            self._repos[attr_name] = repo
            # Makes it available as self.<repo_name>
            setattr(self, attr_name, repo)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self._conn.rollback()
        else:
            await self._conn.commit()
        await self._conn.close()
