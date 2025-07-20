from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError

from auth.schemas import UserDTO
from auth.utils import decode_jwt, get_user_by_email, record_to_model, validate_password
from core.deps import DbInstanceDep


# ===== Аутентификация пользователя через форму (логин, пароль) =====
async def validate_auth_user(
    db: DbInstanceDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> UserDTO:
    """Проверяет логин и пароль пользователя.

    Args:
        db: Экземпляр подключения к базе данных.
        form_data: Данные формы OAuth2 с полями username (email) и password.

    Returns:
        Объект пользователя.

    Raises:
        HTTPException: 401 если пользователь не найден или пароль неверен.
        HTTPException: 403 если пользователь не активен.
    """
    record = await get_user_by_email(db, email=form_data.username)
    if not record or not validate_password(form_data.password, record.get("hashed_password")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid username or password")
    if not record.get("active"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user inactive")
    return record_to_model(record, UserDTO)


AuthUser = Annotated[UserDTO, Depends(validate_auth_user)]


# ===== Аутентификация по токену (OAuth2PasswordBearer) =====
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_token_payload(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    """Извлекает полезную нагрузку токена JWT.

    Args:
        token: Строка токена из запроса.

    Returns:
        Декодированный payload токена.

    Raises:
        HTTPException: 401 если токен недействителен.
    """
    try:
        return decode_jwt(token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token",
        )


async def get_current_auth_user(
    db: DbInstanceDep,
    payload: Annotated[dict, Depends(get_current_token_payload)],
) -> UserDTO:
    """Получает пользователя из базы данных по email из payload токена.

    Args:
        db: Экземпляр подключения к базе данных.
        payload: Расшифрованный payload токена, поле 'sub' содержит email.

    Returns:
        Объект пользователя.

    Raises:
        HTTPException: 401 если пользователь не найден.
    """
    record = await get_user_by_email(db, email=payload.get("sub"))
    if not record:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token user not found")
    return record_to_model(record, UserDTO)


def get_current_active_auth_user(user: Annotated[UserDTO, Depends(get_current_auth_user)]) -> UserDTO:
    """Проверяет, что пользователь активен.

    Args:
        user: Объект пользователя.

    Returns:
        Объект пользователя, если активен.

    Raises:
        HTTPException: 403 если пользователь не активен.
    """
    if user.active:
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user inactive")


ActiveAuthUser = Annotated[UserDTO, Depends(get_current_active_auth_user)]
