from typing import Annotated

from fastapi import Depends

from core.database import Database, db


def get_db() -> Database:
    """Возвращает экземпляр базы данных.

    Returns:
        Экземпляр класса Database, предоставляющий доступ к методам для работы с БД.
    """
    return db


DbInstanceDep = Annotated[Database, Depends(get_db)]
