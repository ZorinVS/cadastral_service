from unittest.mock import AsyncMock, patch

import pytest
from fastapi import status

from api.exceptions import ExternalServiceUnavailable
from auth.deps import get_current_active_auth_user
from core.deps import get_db


@pytest.mark.asyncio
@patch("api.routers.query.save_query_to_db", new_callable=AsyncMock)
@patch("api.routers.query.make_request_to_external", new_callable=AsyncMock)
async def test_submit_query_success(
    mock_make_request,
    mock_save_query,
    cadastral_test_data,
    async_client_factory,
):
    """Тест успешной отправки кадастрового запроса."""
    # Arrange
    external_result = True
    test_data = {**cadastral_test_data, "result": external_result}
    auth_user = AsyncMock()
    mock_db_conn = AsyncMock()
    mock_make_request.return_value = external_result
    mock_save_query.return_value = test_data
    async with async_client_factory(
        dependency_overrides={
            get_db: lambda: mock_db_conn,
            get_current_active_auth_user: lambda: auth_user,
        }
    ) as client:

        # Act
        response = await client.post("/query", json=cadastral_test_data)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == test_data
        mock_make_request.assert_awaited_once()
        mock_save_query.assert_awaited_once()


@pytest.mark.asyncio
@patch("api.routers.query.save_query_to_db", new_callable=AsyncMock)
@patch("api.routers.query.make_request_to_external", new_callable=AsyncMock)
async def test_submit_query_external_service_unavailable(
    mock_make_request,
    mock_save_query,
    cadastral_test_data,
    async_client_factory,
):
    """Тест поведения при недоступном внешнем сервисе."""
    # Arrange
    auth_user = AsyncMock()
    mock_db_conn = AsyncMock()
    mock_make_request.side_effect = ExternalServiceUnavailable("Service down")
    mock_save_query.return_value = None  # т.к. returning=False
    async with async_client_factory(
        dependency_overrides={
            get_db: lambda: mock_db_conn,
            get_current_active_auth_user: lambda: auth_user,
        }
    ) as client:

        # Act
        response = await client.post("/query", json=cadastral_test_data)

        # Assert
        assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
        assert response.json() == {"detail": "Service down"}
        mock_make_request.assert_awaited_once()
        mock_save_query.assert_awaited_once()
