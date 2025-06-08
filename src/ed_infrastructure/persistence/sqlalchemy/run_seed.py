import os

from dotenv import load_dotenv

from ed_infrastructure.persistence.sqlalchemy.db_engine import DbConfig
from ed_infrastructure.persistence.sqlalchemy.seed.main import (async_get,
                                                                async_seed)
from ed_infrastructure.persistence.sqlalchemy.unit_of_work import UnitOfWork


async def main():
    config = _get_config()
    uow = UnitOfWork(config)

    await uow.create_tables()
    await async_seed(uow)
    await async_get(uow)


def _get_config() -> DbConfig:
    load_dotenv()

    return {
        "db": _get_env_variable("POSTGRES_DB"),
        "user": _get_env_variable("POSTGRES_USER"),
        "password": _get_env_variable("POSTGRES_PASSWORD"),
        "host": _get_env_variable("POSTGRES_HOST"),
    }


def _get_env_variable(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise ValueError(f"Environment variable '{name}' is not set.")

    if not isinstance(value, str):
        raise TypeError(f"Environment variable '{name}' must be a string.")

    value = value.strip()
    if not value:
        raise ValueError(f"Environment variable '{name}' cannot be empty.")

    return value


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
