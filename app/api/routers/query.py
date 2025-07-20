from typing import Annotated, List

from fastapi import APIRouter, Body, HTTPException, Query, status

from api.exceptions import ExternalServiceUnavailable
from api.schemas import OrderBy, QueryHistoryResponseDTO, QueryRequestAddDTO, QueryResponseDTO
from api.services import make_request_to_external
from api.utils import save_query_to_db
from auth.deps import ActiveAuthUser
from core.deps import DbInstanceDep

router = APIRouter(tags=["Cadastral Numbers"])

QueryBody = Annotated[QueryRequestAddDTO, Body()]


@router.post(
    "/query",
    response_model=QueryResponseDTO,
    summary="Отправить запрос на внешний сервис",
    description=(
        "Отправляет запрос на внешний сервис и сохраняет результат в базе данных.\n\n"
        "- Если внешний сервис недоступен, сохраняет запрос с `result=None` и возвращает "
        "ошибку `503 Service Unavailable`.\n"
        "- В случае успеха сохраняет результат и возвращает его клиенту."
    ),
)
async def submit_query(request: QueryBody, db: DbInstanceDep, user: ActiveAuthUser) -> QueryResponseDTO:
    params = (request.cadastral_number, request.latitude, request.longitude)

    try:
        result = await make_request_to_external(request)
    except ExternalServiceUnavailable as exc_info:
        await save_query_to_db(db, *params, result=None, returning=False)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc_info),
        )
    inserted_row = await save_query_to_db(db, *params, result=result, returning=True)
    return QueryResponseDTO(**inserted_row)


@router.get(
    "/history",
    response_model=List[QueryHistoryResponseDTO],
    summary="Получить историю запросов",
    description=(
        "Возвращает историю запросов из базы данных с поддержкой:\n\n"
        "- Фильтрации по кадастровому номеру.\n"
        "- Сортировки по дате создания (по возрастанию или убыванию).\n"
        "- Пагинации через параметры `limit` и `offset`."
    ),
)
async def get_history(
    db: DbInstanceDep,
    user: ActiveAuthUser,
    cadastral_number: Annotated[str | None, Query(...)] = None,
    order_by: Annotated[OrderBy, Query(...)] = OrderBy.ascending,
    limit: Annotated[int, Query(..., gt=0, le=100)] = 10,
    offset: Annotated[int, Query(..., ge=0)] = 0,
) -> List[QueryHistoryResponseDTO]:
    query = "SELECT * FROM queries"
    params = []
    param_index = 1

    if cadastral_number:
        query += f"\nWHERE cadastral_number = ${param_index}"
        params.append(cadastral_number)
        param_index += 1

    if order_by == OrderBy.descending:
        query += "\nORDER BY created_at DESC"

    query += f"\nLIMIT ${param_index} OFFSET ${param_index + 1}"
    params.extend([limit, offset])
    param_index += 1

    res = await db.fetch(query, *params)
    return [QueryHistoryResponseDTO(**dict(row)) for row in res]
