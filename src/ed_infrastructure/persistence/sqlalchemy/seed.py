from datetime import UTC, datetime
from typing import TypedDict
from uuid import UUID

from ed_domain.core.aggregate_roots import AuthUser
from ed_domain.core.entities.otp import Otp, OtpType

from ed_infrastructure.common.generic import get_new_id


class Seed(TypedDict):
    otps: list[Otp]
    auth_users: list[AuthUser]


def get_seed():
    seed_data: Seed = {
        "otps": [
            Otp(
                user_id=UUID("620ca27b-c0f9-44a8-b44a-b0a91601b5fe"),
                value="1010",
                otp_type=OtpType.VERIFY_EMAIL,
                expiry_datetime=datetime.now(UTC),
                id=get_new_id(),
                create_datetime=datetime.now(UTC),
                update_datetime=datetime.now(UTC),
                deleted_datetime=datetime.now(UTC),
                deleted=False,
            )
        ],
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
        ],
    }

    return seed_data
