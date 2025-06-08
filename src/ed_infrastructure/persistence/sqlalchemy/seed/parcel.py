from datetime import UTC

from ed_domain.core.entities import Parcel
from ed_domain.core.entities.parcel import ParcelSize
from jsons import datetime

from ed_infrastructure.common.generic import get_new_id


def get_parcel() -> Parcel:
    return Parcel(
        id=get_new_id(),
        size=ParcelSize.SMALL,
        length=10.0,
        width=10.0,
        height=10.0,
        weight=10.0,
        fragile=True,
        create_datetime=datetime.now(UTC),
        update_datetime=datetime.now(UTC),
        deleted_datetime=datetime.now(UTC),
        deleted=False,
    )
