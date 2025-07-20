import pytest
import pytest_asyncio

from api.schemas import QueryRequestAddDTO
from main import app
from tests.utils import test_client_with_overrides


@pytest.fixture(
    params=[
        {"cadastral_number": "77:01:0004010:1234", "latitude": 55.75, "longitude": 37.61},
        {"cadastral_number": "50:21:0004011:5678", "latitude": 56.12, "longitude": 37.35},
        {"cadastral_number": "23:49:0003012:9101", "latitude": 44.62, "longitude": 39.73},
    ]
)
def cadastral_test_data(request):
    """Тестовые данные кадастровых номеров и координат.

    Args:
        request: Фикстура pytest с параметрами.

    Returns:
        Словарь с кадастровым номером и координатами.
    """
    return request.param


@pytest.fixture
def query_request(cadastral_test_data):
    """Объекты DTO для запроса с тестовыми кадастровыми данными.

    Args:
        cadastral_test_data: Тестовые кадастровые данные.

    Returns:
        Объект `QueryRequestAddDTO` с кадастровым номером и координатами.
    """
    return QueryRequestAddDTO(**cadastral_test_data)


@pytest.fixture(params=[{"result": True}, {"result": False}, {"result": None}])
def result_test_data(request):
    """Тестовые данные с возможными значениями результата.

    Args:
        request: Фикстура pytest с параметрами.

    Returns:
        Словарь с ключом 'result' и значением `True`, `False` или `None`.
    """
    return request.param


@pytest_asyncio.fixture
def async_client_factory():
    """Фикстура-фабрика для создания асинхронного HTTP-клиента с возможностью переопределения зависимостей.

    Returns:
        Функция, принимающая словарь переопределений зависимостей (или None)
        и возвращающая асинхронный контекстный менеджер HTTP-клиента.
    """

    def _get_client(*, dependency_overrides):
        return test_client_with_overrides(app=app, dependency_overrides=dependency_overrides)

    return _get_client
