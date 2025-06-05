from typing import TypedDict

import psycopg
from ed_domain.common.logging import get_logger
from psycopg.connection_async import AsyncConnection

from ed_infrastructure.persistence.interfaces import ABCAsyncDbClient


class PsycopgDbConfig(TypedDict):
    user: str
    password: str
    database: str
    host: str


LOG = get_logger()


class PsycopgDbClient(ABCAsyncDbClient):
    def __init__(self, config: PsycopgDbConfig) -> None:
        self._config = config
        self._connection_string = f"dbname={self._config['database']} user={self._config['user']} password={self._config['password']} host={self._config['host']}"

        self._conn: AsyncConnection | None = None

    @property
    def connection(self) -> AsyncConnection:
        if self._conn is None:
            raise RuntimeError(
                "Connection is not established. Call start() first.")
        return self._conn

    async def start(self):
        LOG.info("Starting PsycopgDbClient with config: %s", self._config)

        if self._conn is not None:
            raise RuntimeError(
                "Connection is already established. Call stop() first.")

        self._conn = await psycopg.AsyncConnection.connect(self._connection_string)
        await self._conn.set_autocommit(True)

    async def stop(self):
        if self._conn is None:
            raise RuntimeError(
                "Connection is not established. Call start() first.")

        await self._conn.close()
