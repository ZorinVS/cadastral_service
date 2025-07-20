from fastapi import APIRouter, HTTPException, status

from core.deps import DbInstanceDep

router = APIRouter(tags=["Service Health"])


@router.get(
    "/ping",
    response_model=dict[str, bool],
    summary="Проверка запуска сервера",
    description=(
        "Проверяет, запущен ли сервер и установлено ли соединение с базой данных.\n\n"
        "Возвращает `db_alive: true`, если соединение успешно.\n\n"
        "Если база данных недоступна, возвращается ошибка `503 Service Unavailable`."
    ),
)
async def ping(db: DbInstanceDep) -> dict[str, bool]:
    try:
        row = await db.fetchrow("SELECT 1;")
        return {"db_alive": row is not None and row[0] == 1}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection unavailable",
        )
