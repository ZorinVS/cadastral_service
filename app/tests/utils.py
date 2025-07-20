from contextlib import asynccontextmanager

from httpx import ASGITransport, AsyncClient


@asynccontextmanager
async def test_client_with_overrides(app, dependency_overrides):
    """Асинхронный контекстный менеджер для создания HTTP-клиента с переопределением зависимостей.

    Args:
        app: Экземпляр FastAPI приложения.
        dependency_overrides: Словарь зависимостей для переопределения (опционально).

    Yields:
        Асинхронный HTTP-клиент для тестирования приложения.
    """
    if dependency_overrides:
        app.dependency_overrides.update(dependency_overrides)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

    if dependency_overrides:
        app.dependency_overrides.clear()
