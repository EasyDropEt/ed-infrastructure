import pytest
from ed_domain.validation import ValidationErrorType

from ed_infrastructure.validation.default.phone_number_validator import \
    PhoneNumberValidator


@pytest.fixture
def phone_number_validator():
    return PhoneNumberValidator()


def test_invalid_phone_number_empty(phone_number_validator):
    value = ""
    response = phone_number_validator.validate(value)
    assert response.is_valid is False
    assert response.errors[0]["type"] == ValidationErrorType.MISSING_FIELD


def test_valid_phone_number_with_country_code(phone_number_validator):
    value = "+251912345678"
    response = phone_number_validator.validate(value)
    assert response.is_valid is True
    assert response.errors == []


def test_valid_phone_number_with_country_code_without_plus(phone_number_validator):
    value = "251912345678"
    response = phone_number_validator.validate(value)
    assert response.is_valid is True
    assert response.errors == []


def test_valid_phone_number_without_country_code(phone_number_validator):
    value = "0912345678"
    response = phone_number_validator.validate(value)
    assert response.is_valid is True
    assert response.errors == []


def test_invalid_phone_number_format(phone_number_validator):
    value = "123456"
    response = phone_number_validator.validate(value)
    assert response.is_valid is False
    assert response.errors[0]["type"] == ValidationErrorType.INVALID_VALUE


def test_invalid_phone_number_with_letters(phone_number_validator):
    value = "09123abcde"
    response = phone_number_validator.validate(value)
    assert response.is_valid is False
    assert response.errors[0]["type"] == ValidationErrorType.INVALID_VALUE


def test_invalid_phone_number_with_special_characters(phone_number_validator):
    value = "0912-345-678"
    response = phone_number_validator.validate(value)
    assert response.is_valid is False
    assert response.errors[0]["type"] == ValidationErrorType.INVALID_VALUE
