from datetime import datetime, timedelta, timezone
from typing import Any, Type, TypeVar

import bcrypt
import jwt
from pydantic import BaseModel

from auth.schemas import UserDTO
from core.config import settings
from core.deps import DbInstanceDep


def encode_jwt(
    payload: dict[str, Any],
    private_key: str = settings.jwt.private_key_path.read_text(),
    algorithm: str = settings.jwt.algorithm,
    expire_minutes: int = settings.jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    """Выпускает JWT-токен.

    Args:
        payload: Словарь с полезной нагрузкой токена.
        private_key: Приватный ключ для подписи токена.
        algorithm: Алгоритм шифрования токена.
        expire_minutes: Время жизни токена в минутах.
        expire_timedelta: Альтернативное указание времени жизни токена.

    Returns:
        Подписанный JWT-токен в виде строки.
    """
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    expire = now + (expire_timedelta or timedelta(minutes=expire_minutes))
    to_encode.update(exp=expire, iat=now)
    return jwt.encode(to_encode, private_key, algorithm=algorithm)


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.jwt.public_key_path.read_text(),
    algorithm: str = settings.jwt.algorithm,
) -> Any:
    """Декодирует JWT-токен.

    Args:
        token: Строка или байты токена.
        public_key: Публичный ключ для проверки подписи токена.
        algorithm: Алгоритм, которым был подписан токен.

    Returns:
        Раскодированный payload токена в виде словаря.
    """
    return jwt.decode(token, public_key, algorithms=[algorithm])


def hash_password(password: str) -> str:
    """Хеширует пароль с использованием bcrypt.

    Args:
        password: Открытый текст пароля.

    Returns:
        Хешированный пароль.
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode("utf-8")


def validate_password(password: str, hashed_password: str) -> bool:
    """Проверяет соответствие пароля его хешу.

    Args:
        password: Открытый текст пароля.
        hashed_password: Хешированный пароль.

    Returns:
        True, если пароль верен. Иначе False.
    """
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


async def get_user_by_email(db: DbInstanceDep, email: str) -> UserDTO | None:
    """Ищет пользователя в базе по email.

    Args:
        db: Экземпляр подключения к базе данных.
        email: Email пользователя.

    Returns:
        Объект пользователя или None, если не найден.
    """
    return await db.fetchrow("SELECT * FROM users WHERE email = $1", email)


T = TypeVar("T", bound=BaseModel)


def record_to_model(record: dict[Any, Any], model_class: Type[T]) -> T:
    """Преобразует запись (словарь или подобный объект) в Pydantic-модель.

    Args:
        record: Данные из БД в виде словаря или подобного объекта (например, asyncpg.Record).
        model_class: Класс Pydantic-модели, в которую нужно распарсить данные.

    Returns:
        Экземпляр модели model_class с валидированными полями.
    """
    if not isinstance(record, dict):
        record = dict(record)
    return model_class.parse_obj(record)
