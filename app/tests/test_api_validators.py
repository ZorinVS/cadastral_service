import pytest

from api.validators import CadastralValidator


@pytest.mark.parametrize(
    "new_cn,normalized_cn",
    [
        (" 50 :  45 :  1234567  :   890 ", "50:45:1234567:890"),
        ("77:  99:1234567 :  456 ", "77:99:1234567:456"),
        ("  23 : 45: 7654321:  9999 ", "23:45:7654321:9999"),
    ],
)
def test_new_format_with_cadastral_validator(new_cn, normalized_cn):
    """Проверяет валидацию и нормализацию кадастровых номеров в новом формате."""
    # Act & Assert
    assert CadastralValidator.normalize(new_cn) == normalized_cn
    assert CadastralValidator.is_valid(normalized_cn) is True


@pytest.mark.parametrize(
    "old_cn,normalized_cn",
    [
        (
            " 50 : 45 : 1234567 : 12 : 1 : 1 ",
            "50:45:1234567:12:1:1",
        ),
        ("77 : 99 : 7654321 :  34 : 2 :  3 ", "77:99:7654321:34:2:3"),
        ("  01: 02 :3456789:56: 4:  5", "01:02:3456789:56:4:5"),
    ],
)
def test_old_format_with_cadastral_validator(old_cn, normalized_cn):
    """Проверяет валидацию и нормализацию кадастровых номеров в старом формате."""
    # Act & Assert
    assert CadastralValidator.normalize(old_cn) == normalized_cn
    assert CadastralValidator.is_valid(normalized_cn) is True


@pytest.mark.parametrize(
    "invalid_cn",
    [
        ("50:45:1234567",),  # неверное количество частей (всего 3)
        ("50:45:abcdefg:12",),  # неверный формат чисел
        ("50 45 1234567 890",),  # отсутствует обязательный символ `:`
    ],
)
def test_invalid_format_with_cadastral_validator(invalid_cn):
    """Проверяет отклонение неверных кадастровых номеров."""
    # Act & Assert
    assert CadastralValidator.is_valid(invalid_cn) is False
