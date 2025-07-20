from asyncpg import Record

from core.deps import DbInstanceDep


async def save_query_to_db(
    db: DbInstanceDep,
    cadastral_number: str,
    latitude: float,
    longitude: float,
    result: bool | None,
    returning: bool = True,
) -> Record | None:
    """Сохраняет запрос в базу данных.

    Args:
        db: Экземпляр подключения к базе данных.
        cadastral_number: Кадастровый номер.
        latitude: Широта.
        longitude: Долгота.
        result: Результат выполнения запроса (может быть None, если результат неизвестен).
        returning: Вернуть ли вставленные данные.

    Returns:
        Если returning=True, возвращает строку с сохранёнными данными.
        Если returning=False, возвращает None.∑
    """
    values = (cadastral_number, latitude, longitude, result)
    query = """
        INSERT INTO queries (cadastral_number, latitude, longitude, result)
        VALUES ($1, $2, $3, $4)
    """
    if returning:
        query += """
        RETURNING cadastral_number, latitude, longitude, result
        """
        row = await db.fetchrow(query, *values)
        return row
    else:
        await db.execute(query, *values)
