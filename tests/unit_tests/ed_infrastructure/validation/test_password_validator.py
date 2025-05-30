import pytest
from ed_domain.core.validation import ValidationErrorType

from ed_infrastructure.validation.default.password_validator import \
    PasswordValidator


@pytest.fixture
def password_validator():
    return PasswordValidator()


def test_password_is_required(password_validator):
    dto = ""
    response = password_validator.validate(dto)
    assert not response.is_valid
    assert response.errors[0]["type"] == ValidationErrorType.MISSING_FIELD


def test_password_minimum_length(password_validator):
    dto = "Ab1!"
    response = password_validator.validate(dto)
    assert not response.is_valid
    assert response.errors[0]["type"] == ValidationErrorType.INVALID_VALUE


def test_password_must_include_number(password_validator):
    dto = "Abcdefgh!"
    response = password_validator.validate(dto)
    assert not response.is_valid
    assert response.errors[0]["type"] == ValidationErrorType.INVALID_VALUE


def test_password_must_include_uppercase(password_validator):
    dto = "abcdefgh1!"
    response = password_validator.validate(dto)
    assert not response.is_valid
    assert response.errors[0]["type"] == ValidationErrorType.INVALID_VALUE


def test_password_must_include_lowercase(password_validator):
    dto = "ABCDEFGH1!"
    response = password_validator.validate(dto)
    assert not response.is_valid
    assert response.errors[0]["type"] == ValidationErrorType.INVALID_VALUE


def test_password_must_include_special_character(password_validator):
    dto = "Abcdefgh1"
    response = password_validator.validate(dto)
    assert not response.is_valid
    assert response.errors[0]["type"] == ValidationErrorType.INVALID_VALUE


def test_valid_password(password_validator):
    dto = "Abcdef1!"
    response = password_validator.validate(dto)
    assert response.is_valid
    assert response.errors == []
