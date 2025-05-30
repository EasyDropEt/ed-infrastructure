import pytest
from ed_domain.core.validation import ValidationError, ValidationErrorType

from ed_infrastructure.validation.default.email_validator import EmailValidator


@pytest.fixture
def email_validator():
    return EmailValidator()


def test_email_is_required(email_validator):
    value = ""
    response = email_validator.validate(value)
    assert not response.is_valid
    assert response.errors[0]["type"] == ValidationErrorType.MISSING_FIELD


def test_invalid_email_format(email_validator):
    value = "invalid-email"
    response = email_validator.validate(value)
    assert not response.is_valid
    assert response.errors[0]["type"] == ValidationErrorType.INVALID_VALUE


def test_valid_email(email_validator):
    value = "test@example.com"
    response = email_validator.validate(value)
    assert response.is_valid
    assert response.errors == []
