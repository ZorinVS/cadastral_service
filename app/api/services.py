from httpx import AsyncClient, RequestError

from api.exceptions import ExternalServiceUnavailable
from api.schemas import QueryRequestAddDTO
from core.config import settings


async def make_request_to_external(request: QueryRequestAddDTO) -> bool:
    """Отправляет запрос во внешний сервис для получения результата.

    Args:
        request: DTO с кадастровым номером и координатами.

    Returns:
        True, если внешний сервис вернул положительный результат. Иначе False.

    Raises:
        ExternalServiceUnavailable: Если внешний сервис недоступен или произошла ошибка запроса.
    """
    try:
        async with AsyncClient() as ac:
            external_service_url = f"{settings.EXTERNAL_SERVICE_HOST}/result"
            response = await ac.post(
                external_service_url,
                json={
                    "cadastral_number": request.cadastral_number,
                    "latitude": request.latitude,
                    "longitude": request.longitude,
                },
            )
            return response.json()["result"]
    except RequestError:
        raise ExternalServiceUnavailable("External service temporarily unavailable")
