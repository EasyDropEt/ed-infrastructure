from ed_domain.core.aggregate_roots.order import Order
from ed_domain.persistence.async_repositories.abc_async_order_repository import \
    ABCAsyncOrderRepository

from ed_infrastructure.persistence.sqlalchemy.models import OrderModel
from ed_infrastructure.persistence.sqlalchemy.repositories.bill_repository import \
    BillRepository
from ed_infrastructure.persistence.sqlalchemy.repositories.business_repository import \
    BusinessRepository
from ed_infrastructure.persistence.sqlalchemy.repositories.consumer_repository import \
    ConsumerRepository
from ed_infrastructure.persistence.sqlalchemy.repositories.driver_repository import \
    DriverRepository
from ed_infrastructure.persistence.sqlalchemy.repositories.generic_repository import \
    AsyncGenericRepository
from ed_infrastructure.persistence.sqlalchemy.repositories.parcel_repository import \
    ParcelRepository


class OrderRepository(
    ABCAsyncOrderRepository,
    AsyncGenericRepository[Order, OrderModel],
):
    def __init__(self) -> None:
        super().__init__(OrderModel)

    @classmethod
    def _to_entity(cls, model: OrderModel) -> Order:
        return Order(
            id=model.id,
            business=BusinessRepository._to_entity(model.business),
            consumer=ConsumerRepository._to_entity(model.consumer),
            driver=DriverRepository._to_entity(
                model.driver) if model.driver else None,
            bill=BillRepository._to_entity(model.bill),
            parcel=ParcelRepository._to_entity(model.parcel),
            latest_time_of_delivery=model.latest_time_of_delivery,
            order_status=model.order_status,
            create_datetime=model.create_datetime,
            update_datetime=model.update_datetime,
            deleted=model.deleted,
            deleted_datetime=model.deleted_datetime,
        )

    @classmethod
    def _to_model(cls, entity: Order) -> OrderModel:
        return OrderModel(
            id=entity.id,
            business_id=entity.business.id,
            consumer_id=entity.consumer.id,
            driver_id=entity.driver.id if entity.driver else None,
            bill_id=entity.bill.id,
            parcel_id=entity.parcel.id,
            latest_time_of_delivery=entity.latest_time_of_delivery,
            order_status=entity.order_status,
            create_datetime=entity.create_datetime,
            update_datetime=entity.update_datetime,
            deleted=entity.deleted,
            deleted_datetime=entity.deleted_datetime,
        )
