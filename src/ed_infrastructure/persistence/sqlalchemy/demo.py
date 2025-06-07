import os

from dotenv import load_dotenv

from ed_infrastructure.persistence.sqlalchemy.db_engine import DbConfig
from ed_infrastructure.persistence.sqlalchemy.seed import get_seed
from ed_infrastructure.persistence.sqlalchemy.unit_of_work import UnitOfWork


def get_config() -> DbConfig:
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


async def seed():
    config = get_config()
    seed_data = get_seed()

    print(config)
    uow = UnitOfWork(config)

    await uow.create_tables()

    async with uow.transaction():
        created_users = await uow.auth_user_repository.create_many(
            seed_data["auth_users"]
        )

        for user in created_users:
            print("CREATED:", user)


async def get_auth_users():
    config = get_config()

    print(config)
    uow = UnitOfWork(config)

    async with uow.transaction():
        users = await uow.auth_user_repository.get_all()

        for user in users:
            print(user)


if __name__ == "__main__":
    import asyncio

    asyncio.run(get_auth_users())
