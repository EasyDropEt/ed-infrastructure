import pytest
from ed_domain.core.validation import ValidationErrorType

from ed_infrastructure.validation.default.amount_validator import \
    AmountValidator


@pytest.fixture
def amount_validator() -> AmountValidator:
    return AmountValidator()


@pytest.mark.parametrize(
    ["amount"],
    [
        (10,),
        (100.0,),
        (12.25,),
    ],
)
def test_valid_amount(amount, amount_validator: AmountValidator):
    response = amount_validator.validate(amount)
    assert response.is_valid


@pytest.mark.parametrize(
    ["amount"],
    [
        (-10,),
        (-100,),
    ],
)
def test_invalid_amount_invalid_length(amount, amount_validator):
    response = amount_validator.validate(amount)
    assert not response.is_valid
    assert response.errors[0]["type"] == ValidationErrorType.INVALID_VALUE


@pytest.mark.parametrize(
    ["amount"],
    [
        (1000000.1,),
        (10000000,),
    ],
)
def test_invalid_amount_non_numeric(amount, amount_validator):
    response = amount_validator.validate(amount)
    assert not response.is_valid
    assert response.errors[0]["type"] == ValidationErrorType.INVALID_VALUE
