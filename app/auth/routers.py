from fastapi import APIRouter, HTTPException, status

from auth.deps import AuthUser
from auth.schemas import MessageResponse, TokenInfo, UserRegisterDTO
from auth.utils import encode_jwt, hash_password
from core.deps import DbInstanceDep

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=MessageResponse,
    summary="Регистрация нового пользователя",
    description=(
        "Регистрирует нового пользователя по указанному email и паролю.\n\n"
        "- Если пользователь с таким email уже существует, возвращает ошибку 409.\n"
        "- Пароль хешируется перед сохранением в базе данных."
    ),
)
async def register(data: UserRegisterDTO, db: DbInstanceDep) -> MessageResponse:
    existing = await db.fetch("SELECT id FROM users WHERE email = $1", data.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    hashed = hash_password(data.password)
    await db.execute("INSERT INTO users (email, hashed_password) VALUES ($1, $2)", data.email, hashed)
    return MessageResponse(message="User registered successfully")


@router.post(
    "/login",
    response_model=TokenInfo,
    summary="Авторизация пользователя и выдача JWT",
    description=(
        "Авторизует пользователя и возвращает JWT access токен.\n\n"
        "- В качестве логина используется email, пароль проверяется на соответствие.\n"
        "- В случае успешной аутентификации возвращается токен для последующих запросов.\n"
        "- Формат токена: Bearer."
    ),
)
def login(user: AuthUser) -> TokenInfo:
    token = encode_jwt(
        payload={
            "sub": user.email,
            "email": user.email,
        }
    )
    return TokenInfo(access_token=token, token_type="Bearer")
