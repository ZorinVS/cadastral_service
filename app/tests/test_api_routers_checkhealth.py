from typing import Any, AsyncContextManager, Callable
from unittest.mock import AsyncMock

import pytest
from fastapi import status
from httpx import AsyncClient

from core.deps import get_db


@pytest.mark.asyncio
async def test_ping_db_alive(
    async_client_factory: Callable[
        [dict[Callable[..., Any], Callable[..., Any]] | None], AsyncContextManager[AsyncClient]
    ],
):
    """Тестирует успешный пинг базы данных."""
    # Arrange
    mock_db = AsyncMock()
    mock_db.fetchrow.return_value = (1,)

    # Act
    async with async_client_factory(dependency_overrides={get_db: lambda: mock_db}) as client:
        response = await client.get("/ping")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"db_alive": True}


@pytest.mark.asyncio
async def test_ping_db_unavailable(
    async_client_factory: Callable[
        [dict[Callable[..., Any], Callable[..., Any]] | None], AsyncContextManager[AsyncClient]
    ],
):
    """Тестирует поведение при недоступной базе данных."""
    # Arrange
    mock_db = AsyncMock()
    mock_db.fetchrow.side_effect = Exception("DB down")

    # Act
    async with async_client_factory(dependency_overrides={get_db: lambda: mock_db}) as client:
        response = await client.get("/ping")

    # Assert
    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert response.json()["detail"] == "Database connection unavailable"
