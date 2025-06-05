from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from ed_domain.core.aggregate_roots import AuthUser

from ed_infrastructure.persistence.psycopg.models.base_model import BaseModel


@dataclass
class AuthUserModel(BaseModel[AuthUser]):
    id: UUID
    first_name: str
    last_name: str
    password_hash: str
    verified: bool
    logged_in: bool
    email: str | None
    phone_number: str | None
    create_datetime: datetime
    update_datetime: datetime
    deleted: bool

    @classmethod
    def get_columns(cls) -> list[str]:
        return list(cls.__dataclass_fields__.keys())

    @classmethod
    def from_row_to_entity(cls, row: dict) -> AuthUser:
        return AuthUser(
            id=row["id"],
            first_name=row["first_name"],
            last_name=row["last_name"],
            password_hash=row["password_hash"],
            verified=row["verified"],
            logged_in=row["logged_in"],
            email=row["email"],
            phone_number=row["phone_number"],
            create_datetime=row["create_datetime"],
            update_datetime=row["update_datetime"],
            deleted=row["deleted"],
        )

    @classmethod
    def from_entity(cls, entity: AuthUser) -> "AuthUserModel":
        return cls(
            id=entity.id,
            first_name=entity.first_name,
            last_name=entity.last_name,
            password_hash=entity.password_hash,
            verified=entity.verified,
            logged_in=entity.logged_in,
            email=entity.email,
            phone_number=entity.phone_number,
            create_datetime=entity.create_datetime,
            update_datetime=entity.update_datetime,
            deleted=entity.deleted,
        )

    def to_entity(self) -> AuthUser:
        return AuthUser(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            password_hash=self.password_hash,
            verified=self.verified,
            logged_in=self.logged_in,
            email=self.email,
            phone_number=self.phone_number,
            create_datetime=self.create_datetime,
            update_datetime=self.update_datetime,
            deleted=self.deleted,
        )

    def to_dict(self) -> dict:
        return {
            **self.__dict__,
            "id": str(self.id),
        }  # Convert UUID to string for JSON serialization
