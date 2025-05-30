import pytest
from ed_domain.core.validation import ValidationErrorType

from ed_infrastructure.validation.default.otp_validator import OtpValidator


@pytest.fixture
def otp_validator() -> OtpValidator:
    return OtpValidator()


def test_valid_otp(otp_validator: OtpValidator):
    response = otp_validator.validate("1234")
    assert response.is_valid


@pytest.mark.parametrize(
    ["otp"],
    [
        ("12345",),
        ("123",),
    ],
)
def test_invalid_otp_invalid_length(otp, otp_validator):
    response = otp_validator.validate(otp)
    assert not response.is_valid
    assert response.errors[0]["type"] == ValidationErrorType.INVALID_VALUE


@pytest.mark.parametrize(
    ["otp"],
    [
        ("abcd",),
        ("1a2b",),
        ("    ",),
    ],
)
def test_invalid_otp_non_numeric(otp, otp_validator):
    response = otp_validator.validate(otp)
    assert not response.is_valid
    assert response.errors[0]["type"] == ValidationErrorType.INVALID_TYPE
