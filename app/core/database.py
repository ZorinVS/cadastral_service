from typing import Any

import asyncpg
from asyncpg import Pool, Record


class Database:
    """Класс для работы с подключением к базе данных через пул соединений."""

    def __init__(self) -> None:
        """Инициализирует пустой пул соединений."""
        self.pool: Pool | None = None

    async def connect(self, dsn: str) -> None:
        """Устанавливает соединение с базой данных и создаёт пул соединений.

        Args:
            dsn: Строка подключения к базе данных.
        """
        self.pool = await asyncpg.create_pool(dsn=dsn)

    async def disconnect(self) -> None:
        """Закрывает пул соединений с базой данных."""
        if self.pool:
            await self.pool.close()

    def _get_pool(self) -> Pool:
        """Возвращает пул соединений с базой данных.

        Returns:
            Пул соединений.

        Raises:
            AssertionError: Если соединение не установлено.
        """
        assert self.pool is not None
        return self.pool

    async def execute(self, query: str, *args: Any) -> Any:
        """Выполняет SQL-запрос на изменение данных (INSERT, UPDATE, DELETE).

        Args:
            query: SQL-запрос.
            *args: Параметры для запроса.

        Returns:
            Результат выполнения запроса.
        """
        async with self._get_pool().acquire() as conn:
            return await conn.execute(query, *args)

    async def fetch(self, query: str, *args: Any) -> Any:
        """Выполняет SQL-запрос и возвращает все найденные строки.

        Args:
            query: SQL-запрос.
            *args: Параметры для запроса.

        Returns:
            Список строк результата.
        """
        async with self._get_pool().acquire() as conn:
            return await conn.fetch(query, *args)

    async def fetchrow(self, query: str, *args: Any) -> Record | None:
        """Выполняет SQL-запрос и возвращает одну строку результата.

        Args:
            query: SQL-запрос.
            *args: Параметры для запроса.

        Returns:
            Одна строка результата или None.
        """
        async with self._get_pool().acquire() as conn:
            return await conn.fetchrow(query, *args)


db = Database()
