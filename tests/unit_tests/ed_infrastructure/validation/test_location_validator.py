import pytest
from ed_domain.validation import ValidationErrorType

from ed_infrastructure.validation.default.location_validator import (
    LatitudeValidator, LongitudeValidator)


@pytest.fixture
def latitude_validator() -> LatitudeValidator:
    return LatitudeValidator()


@pytest.fixture
def longitude_validator() -> LongitudeValidator:
    return LongitudeValidator()


@pytest.mark.parametrize(
    ["location"],
    [
        (9.0,),
        (8.9,),
        (8.8,),
        (9.1,),
        (8.92,),
    ],
)
def test_valid_latitude(location, latitude_validator):
    response = latitude_validator.validate(location)
    assert response.is_valid


@pytest.mark.parametrize(
    ["location"],
    [
        (9.8,),
        (9.2,),
        (8.7,),
        (8.79,),
    ],
)
def test_invalid_latitude(location, latitude_validator):
    response = latitude_validator.validate(location)
    assert not response.is_valid
    assert response.errors[0]["type"] == ValidationErrorType.INVALID_VALUE


@pytest.mark.parametrize(
    ["location"],
    [
        (38.6,),
        (39.0,),
        (38.7,),
        (38.9,),
    ],
)
def test_valid_longitude(location, longitude_validator):
    response = longitude_validator.validate(location)
    assert response.is_valid


@pytest.mark.parametrize(
    ["location"],
    [
        (38.5,),
        (39.1,),
        (38.4,),
        (39.2,),
    ],
)
def test_invalid_longitude(location, longitude_validator):
    response = longitude_validator.validate(location)
    assert not response.is_valid
    assert response.errors[0]["type"] == ValidationErrorType.INVALID_VALUE
