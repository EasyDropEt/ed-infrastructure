from ed_domain.core.aggregate_roots import AuthUser
from ed_domain.persistence.async_repositories.abc_async_auth_user_repository import \
    ABCAsyncAuthUserRepository

from ed_infrastructure.persistence.psycopg.db_client import PsycopgDbClient
from ed_infrastructure.persistence.psycopg.models.auth_user_model import \
    AuthUserModel
from ed_infrastructure.persistence.psycopg.repositories.generic_repository import \
    GenericRepository


class AuthUserRepository(
    GenericRepository[AuthUser, AuthUserModel], ABCAsyncAuthUserRepository
):
    def __init__(self, db_client: PsycopgDbClient) -> None:
        super().__init__(db_client, AuthUserModel, "auth_user")
