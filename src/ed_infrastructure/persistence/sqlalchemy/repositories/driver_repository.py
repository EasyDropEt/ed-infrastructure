from ed_domain.core.aggregate_roots.driver import Driver
from ed_domain.persistence.async_repositories.abc_async_driver_repository import \
    ABCAsyncDriverRepository

from ed_infrastructure.persistence.sqlalchemy.models import DriverModel
from ed_infrastructure.persistence.sqlalchemy.repositories.car_repository import \
    CarRepository
from ed_infrastructure.persistence.sqlalchemy.repositories.generic_repository import \
    AsyncGenericRepository
from ed_infrastructure.persistence.sqlalchemy.repositories.location_repository import \
    LocationRepository


class DriverRepository(
    ABCAsyncDriverRepository, AsyncGenericRepository[Driver, DriverModel]
):
    def __init__(self) -> None:
        super().__init__(DriverModel)

    @classmethod
    def _to_entity(cls, model: DriverModel) -> Driver:
        return Driver(
            id=model.id,
            user_id=model.user.id,
            first_name=model.first_name,
            last_name=model.last_name,
            profile_image=model.profile_image,
            phone_number=model.phone_number,
            current_location=LocationRepository._to_entity(
                model.current_location),
            car=CarRepository._to_entity(model.car),
            create_datetime=model.create_datetime,
            update_datetime=model.update_datetime,
            deleted=model.deleted,
            deleted_datetime=model.deleted_datetime,
        )

    @classmethod
    def _to_model(cls, entity: Driver) -> DriverModel:
        return DriverModel(
            id=entity.id,
            user_id=entity.user_id,
            first_name=entity.first_name,
            last_name=entity.last_name,
            profile_image=entity.profile_image,
            phone_number=entity.phone_number,
            current_location_id=entity.current_location.id,
            car_id=entity.car.id,
            available=entity.available,
            email=entity.email,
            create_datetime=entity.create_datetime,
            update_datetime=entity.update_datetime,
            deleted=entity.deleted,
            deleted_datetime=entity.deleted_datetime,
        )
