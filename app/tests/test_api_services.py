from unittest.mock import AsyncMock, patch

import httpx
import pytest
from fastapi import status

from api.exceptions import ExternalServiceUnavailable
from api.services import make_request_to_external


@pytest.mark.asyncio
@patch("httpx.AsyncClient.post", new_callable=AsyncMock)
async def test_getting_positive_result(mock_post, query_request, async_client_factory):
    """Тест получения положительного результата от внешнего сервиса."""
    # Arrange
    positive_result = True
    mock_response = httpx.Response(
        status_code=status.HTTP_200_OK,
        json={"result": positive_result},
    )
    mock_post.return_value = mock_response

    # Act
    res = await make_request_to_external(query_request)

    # Assert
    assert res is positive_result
    mock_post.assert_awaited_once()


@pytest.mark.asyncio
@patch("httpx.AsyncClient.post", new_callable=AsyncMock)
async def test_getting_negative_result(mock_post, query_request, async_client_factory):
    """Тест получения отрицательного результата от внешнего сервиса."""
    # Arrange
    negative_result = False
    mock_response = httpx.Response(
        status_code=status.HTTP_200_OK,
        json={"result": negative_result},
    )
    mock_post.return_value = mock_response

    # Act
    res = await make_request_to_external(query_request)

    # Assert
    assert res is negative_result
    mock_post.assert_awaited_once()


@pytest.mark.asyncio
@patch("httpx.AsyncClient.post", new_callable=AsyncMock)
async def test_service_unavailable(mock_post, query_request, async_client_factory):
    """Тест обработки ошибки запроса к внешнему сервису."""
    # Arrange
    mock_post.side_effect = httpx.RequestError("Some request error")
    expected_exc_info = "External service temporarily unavailable"

    # Act & Assert
    with pytest.raises(ExternalServiceUnavailable, match=expected_exc_info):
        await make_request_to_external(query_request)

    # Assert
    mock_post.assert_awaited_once()
