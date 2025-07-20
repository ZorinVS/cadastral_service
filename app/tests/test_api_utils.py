from unittest.mock import AsyncMock

import pytest

from api.utils import save_query_to_db


@pytest.mark.asyncio
async def test_save_query_to_db_with_returning(cadastral_test_data, result_test_data):
    """Тестирует сохранение запроса в БД с флагом returning=True."""
    # Arrange
    mock_db = AsyncMock()
    expected_result = {**cadastral_test_data, **result_test_data}
    mock_db.fetchrow.return_value = expected_result

    # Act
    result = await save_query_to_db(
        db=mock_db,
        cadastral_number=cadastral_test_data["cadastral_number"],
        latitude=cadastral_test_data["latitude"],
        longitude=cadastral_test_data["longitude"],
        result=result_test_data["result"],
        returning=True,
    )

    # Assert
    mock_db.fetchrow.assert_awaited_once()
    assert result == expected_result


@pytest.mark.asyncio
async def test_save_query_to_db_without_returning(cadastral_test_data, result_test_data):
    """Тестирует сохранение запроса в БД с флагом returning=False."""
    # Arrange
    mock_db = AsyncMock()
    mock_db.execute.return_value = None
    test_data = {**cadastral_test_data, **result_test_data, "returning": False}

    # Act
    result = await save_query_to_db(db=mock_db, **test_data)

    # Assert
    mock_db.execute.assert_awaited_once()
    assert result is None
