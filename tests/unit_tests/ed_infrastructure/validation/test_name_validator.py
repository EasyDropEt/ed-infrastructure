import pytest
from ed_domain.validation import ValidationErrorType

from ed_infrastructure.validation.default.name_validator import NameValidator


@pytest.fixture
def name_validator() -> NameValidator:
    return NameValidator()


def test_invalid_missing_name(name_validator: NameValidator):
    dto = ""
    response = name_validator.validate(dto)
    assert not response.is_valid
    assert response.errors[0]["type"] == ValidationErrorType.MISSING_FIELD


@pytest.mark.parametrize(
    ["name"],
    [
        ("Abebe",),
        ("Meseret",),
        ("Tesfaye",),
    ],
)
def test_valid_name(name, name_validator: NameValidator):
    response = name_validator.validate(name)
    assert response.is_valid


@pytest.mark.parametrize(
    ["name"],
    [
        ("A",),
        ("Abcdefghijklmnopqrstuvwxyz",),
        ("A B C D E F G H I J K L M N O P Q R S T U V W X Y Z",),
        ("Abebe Tesfaye",),
        ("Meseret Abebe",),
        ("Tes,a",),
    ],
)
def test_invalid_name_invalid_length(name, name_validator):
    response = name_validator.validate(name)
    assert not response.is_valid
    assert response.errors[0]["type"] == ValidationErrorType.INVALID_VALUE
