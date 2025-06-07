from datetime import UTC, datetime
from typing import TypedDict

from ed_domain.core.aggregate_roots import AuthUser

from ed_infrastructure.common.generic import get_new_id


class Seed(TypedDict):
    auth_users: list[AuthUser]


def get_seed():
    seed_data: Seed = {
        "auth_users": [
            AuthUser(
                id=get_new_id(),
                first_name="Fikernew",
                last_name="Birhanu",
                phone_number="251930316620",
                email="phikernew0808@gmail.com",
                password_hash="$2b$12$mlewRx4nfy7FKCB.RJrVs.N.CD95q3DBBDr6zqxtOzQoBvQjnzFK6",
                verified=True,
                logged_in=False,
                create_datetime=datetime.now(UTC),
                update_datetime=datetime.now(UTC),
                deleted_datetime=datetime.now(UTC),
                deleted=False,
            ),
            AuthUser(
                id=get_new_id(),
                first_name="Firaol",
                last_name="Ibrahim",
                phone_number="251977346620",
                email="firaolibrahim28@gmail.com",
                password_hash="$2b$12$mlewRx4nfy7FKCB.RJrVs.N.CD95q3DBBDr6zqxtOzQoBvQjnzFK6",
                verified=True,
                logged_in=False,
                create_datetime=datetime.now(UTC),
                update_datetime=datetime.now(UTC),
                deleted_datetime=datetime.now(UTC),
                deleted=False,
            ),
            AuthUser(
                id=get_new_id(),
                first_name="Shamil",
                last_name="Bedru",
                phone_number="251977346620",
                email="shamilbedru47@gmail.com",
                password_hash="$2b$12$mlewRx4nfy7FKCB.RJrVs.N.CD95q3DBBDr6zqxtOzQoBvQjnzFK6",
                verified=True,
                logged_in=False,
                create_datetime=datetime.now(UTC),
                update_datetime=datetime.now(UTC),
                deleted_datetime=datetime.now(UTC),
                deleted=False,
            ),
        ]
    }

    return seed_data
