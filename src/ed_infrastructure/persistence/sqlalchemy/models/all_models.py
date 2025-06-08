from datetime import datetime
from uuid import UUID

from ed_domain.core.aggregate_roots.delivery_job import DeliveryJobStatus
from ed_domain.core.aggregate_roots.order import OrderStatus
from ed_domain.core.aggregate_roots.waypoint import (WaypointStatus,
                                                     WaypointType)
from ed_domain.core.entities.api_key import ApiKeyStatus
from ed_domain.core.entities.bill import BillStatus
from ed_domain.core.entities.notification import NotificationType
from ed_domain.core.entities.otp import OtpType
from ed_domain.core.entities.parcel import ParcelSize
from sqlalchemy import (Boolean, DateTime, Double, Enum, Float, ForeignKey,
                        Integer, String)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ed_infrastructure.persistence.sqlalchemy.models.base_model import \
    BaseModel


class ApiKeyModel(BaseModel):
    __tablename__ = "api_key"

    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    prefix: Mapped[str] = mapped_column(String)
    key_hash: Mapped[str] = mapped_column(String)
    status: Mapped[ApiKeyStatus] = mapped_column(Enum(ApiKeyStatus))

    # Relationships
    business_id: Mapped[UUID] = mapped_column(ForeignKey("business.id"))


class AdminModel(BaseModel):
    __tablename__ = "admin"

    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)

    # Relationships
    user_id: Mapped[UUID] = mapped_column(ForeignKey("auth_user.id"))
    user: Mapped["AuthUserModel"] = relationship(uselist=False, lazy="joined")


class AuthUserModel(BaseModel):
    __tablename__ = "auth_user"

    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    password_hash: Mapped[str] = mapped_column(String)
    verified: Mapped[bool] = mapped_column(Boolean)
    logged_in: Mapped[bool] = mapped_column(Boolean)
    email: Mapped[str | None] = mapped_column(String, nullable=True)
    phone_number: Mapped[str | None] = mapped_column(String, nullable=True)

    # Relationships
    notifications: Mapped[list["NotificationModel"]
                          ] = relationship(lazy="selectin")
    otps: Mapped[list["OtpModel"]] = relationship(lazy="selectin")


class BillModel(BaseModel):
    __tablename__ = "bill"

    amount_in_birr: Mapped[float] = mapped_column(Double, nullable=False)
    bill_status: Mapped[BillStatus] = mapped_column(
        Enum(BillStatus), nullable=False)
    due_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False)

    # Relationship
    order: Mapped["OrderModel"] = relationship(
        uselist=False, back_populates="bill", lazy="joined"
    )


class BusinessModel(BaseModel):
    __tablename__ = "business"

    business_name: Mapped[str] = mapped_column(String, nullable=False)
    owner_first_name: Mapped[str] = mapped_column(String, nullable=False)
    owner_last_name: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)

    # Relationships
    user_id: Mapped[UUID] = mapped_column(ForeignKey("auth_user.id"))
    user: Mapped["AuthUserModel"] = relationship(uselist=False, lazy="joined")

    location_id: Mapped[UUID] = mapped_column(ForeignKey("location.id"))
    location: Mapped["LocationModel"] = relationship(
        uselist=False, lazy="joined")

    orders: Mapped[list["OrderModel"]] = relationship(
        back_populates="business", lazy="selectin"
    )

    api_keys: Mapped[list["ApiKeyModel"]] = relationship(lazy="selectin")


class CarModel(BaseModel):
    __tablename__ = "car"

    make: Mapped[str] = mapped_column(String, nullable=False)
    model: Mapped[str] = mapped_column(String, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    registration_number: Mapped[str] = mapped_column(String, nullable=False)
    license_plate_number: Mapped[str] = mapped_column(String, nullable=False)
    color: Mapped[str] = mapped_column(String, nullable=False)
    seats: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationships
    driver: Mapped["DriverModel"] = relationship(
        "DriverModel", uselist=False, back_populates="car", lazy="joined"
    )


class ConsumerModel(BaseModel):
    __tablename__ = "consumer"

    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[str] = mapped_column(String, nullable=False)
    profile_image_url: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)

    # Relationships
    user_id: Mapped[UUID] = mapped_column(ForeignKey("auth_user.id"))
    user: Mapped["AuthUserModel"] = relationship(
        "AuthUserModel", uselist=False, lazy="joined"
    )
    location_id: Mapped[UUID] = mapped_column(ForeignKey("location.id"))
    location: Mapped["LocationModel"] = relationship(
        "LocationModel", uselist=False, lazy="joined"
    )

    orders: Mapped[list["OrderModel"]] = relationship(
        "OrderModel", back_populates="consumer", lazy="selectin"
    )


class DeliveryJobModel(BaseModel):
    __tablename__ = "delivery_job"

    estimated_payment_in_birr: Mapped[float] = mapped_column(
        Float, nullable=False)
    estimated_completion_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    estimated_distance_in_kms: Mapped[float] = mapped_column(
        Double, nullable=False)
    estimated_time_in_minutes: Mapped[int] = mapped_column(
        Integer, nullable=False)
    status: Mapped[DeliveryJobStatus] = mapped_column(
        String(50), nullable=False)

    # Relationships
    driver_id: Mapped[UUID] = mapped_column(ForeignKey("driver.id"))
    driver: Mapped["DriverModel"] = relationship(
        uselist=False, back_populates="delivery_jobs", lazy="joined"
    )

    waypoints: Mapped[list["WaypointModel"]] = relationship(lazy="selectin")


class DriverModel(BaseModel):
    __tablename__ = "driver"

    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    profile_image: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[str] = mapped_column(String, nullable=False)
    available: Mapped[bool] = mapped_column(Boolean, nullable=False)
    email: Mapped[str | None] = mapped_column(String, nullable=False)

    # Relationships
    user_id: Mapped[UUID] = mapped_column(ForeignKey("auth_user.id"))
    user: Mapped["AuthUserModel"] = relationship(
        "AuthUserModel", uselist=False, lazy="joined"
    )

    current_location_id: Mapped[UUID] = mapped_column(
        ForeignKey("location.id"))
    current_location: Mapped["LocationModel"] = relationship(
        "LocationModel", uselist=False, lazy="joined"
    )

    car_id: Mapped[UUID] = mapped_column(ForeignKey("car.id"))
    car: Mapped["CarModel"] = relationship(
        "CarModel", uselist=False, back_populates="driver", lazy="joined"
    )

    orders: Mapped[list["OrderModel"]] = relationship(
        "OrderModel", back_populates="driver", lazy="selectin"
    )
    delivery_jobs: Mapped[list["DeliveryJobModel"]] = relationship(
        "DeliveryJobModel", back_populates="driver", lazy="selectin"
    )


class LocationModel(BaseModel):
    __tablename__ = "location"

    address: Mapped[str] = mapped_column(String, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    postal_code: Mapped[str] = mapped_column(String, nullable=False)
    city: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str] = mapped_column(String, nullable=False)
    last_used: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), nullable=False
    )


class NotificationModel(BaseModel):
    __tablename__ = "notification"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("auth_user.id"))
    notification_type: Mapped[NotificationType] = mapped_column(
        Enum(NotificationType), nullable=False
    )
    message: Mapped[str] = mapped_column(String, nullable=False)
    read_status: Mapped[bool] = mapped_column(Boolean, nullable=False)


class OrderModel(BaseModel):
    __tablename__ = "order"

    latest_time_of_delivery: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    order_status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus), nullable=False)

    # Relationships
    delivery_job_id: Mapped[UUID] = mapped_column(
        ForeignKey("delivery_job.id"), nullable=True
    )

    business_id: Mapped[UUID] = mapped_column(ForeignKey("business.id"))
    business: Mapped["BusinessModel"] = relationship(
        "BusinessModel", uselist=False, back_populates="orders", lazy="joined"
    )

    consumer_id: Mapped[UUID] = mapped_column(ForeignKey("consumer.id"))
    consumer: Mapped["ConsumerModel"] = relationship(
        "ConsumerModel", uselist=False, back_populates="orders", lazy="joined"
    )

    driver_id: Mapped[UUID] = mapped_column(
        ForeignKey("driver.id"), nullable=True)
    driver: Mapped["DriverModel"] = relationship(
        "DriverModel", uselist=False, back_populates="orders", lazy="joined"
    )

    bill_id: Mapped[UUID] = mapped_column(ForeignKey("bill.id"))
    bill: Mapped["BillModel"] = relationship(
        uselist=False, back_populates="order", lazy="joined"
    )

    parcel_id: Mapped[UUID] = mapped_column(ForeignKey("parcel.id"))
    parcel: Mapped["ParcelModel"] = relationship(uselist=False, lazy="joined")


class OtpModel(BaseModel):
    __tablename__ = "otp"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("auth_user.id"))
    otp_type: Mapped[OtpType] = mapped_column(Enum(OtpType), nullable=False)
    value: Mapped[str] = mapped_column(String, nullable=False)
    expiry_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )


class ParcelModel(BaseModel):
    __tablename__ = "parcel"

    size: Mapped[ParcelSize] = mapped_column(Enum(ParcelSize), nullable=False)
    length: Mapped[float] = mapped_column(Float, nullable=False)
    width: Mapped[float] = mapped_column(Float, nullable=False)
    height: Mapped[float] = mapped_column(Float, nullable=False)
    weight: Mapped[float] = mapped_column(Float, nullable=False)
    fragile: Mapped[bool] = mapped_column(Boolean, nullable=False)

    # Relationships
    ...


class WaypointModel(BaseModel):
    __tablename__ = "waypoint"

    expected_arrival_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    actual_arrival_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    sequence: Mapped[int] = mapped_column(Integer, nullable=False)
    waypoint_type: Mapped[WaypointType] = mapped_column(
        Enum(WaypointType), nullable=False
    )
    waypoint_status: Mapped[WaypointStatus] = mapped_column(
        Enum(WaypointStatus), nullable=False
    )

    # Relationships
    order_id: Mapped[UUID] = mapped_column(ForeignKey("order.id"))
    order: Mapped["OrderModel"] = relationship(
        "OrderModel", uselist=False, lazy="joined"
    )

    delivery_job_id: Mapped[UUID] = mapped_column(
        ForeignKey("delivery_job.id"))
