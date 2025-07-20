# Cadastral Service — FastAPI-сервис

---


## Техническое задание


### Цель проекта

Разработать web-сервис, который принимает запрос с кадастровым номером, 
широтой и долготой, эмулирует запрос к внешнему серверу с возможной задержкой 
до 60 секунд, сохраняет данные запроса и ответа в базе данных и предоставляет API 
для просмотра истории запросов.

### Описание функционала

#### Основные требования:

1. Приём запросов с кадастровым номером, широтой и долготой.
2. Эмуляция отправки этих данных на внешний сервер. Задержка до 60 секунд, ответ `true` или `false`.
3. Сохранение запросов и ответов в БД.
4. Предоставить API для:
    - проверки работоспособности сервера,
    - отправки кадастрового номера с координатами,
    - получения полной истории всех запросов,
    - получения истории по конкретному кадастровому номеру.

#### Дополнительные требования:

5. Регистрация пользователей и аутентификация.
6. Валидация входящих данных.
7. Покрытие тестами (pytest).

### Необходимый стек

- Python 3.9+
- FastAPI (async-роуты)
- PostgreSQL
- asyncpg (async запросы)
- Alembic / raw SQL migrations
- Docker
- Docker Compose
- Pytest

---


## Структура проекта (обзорная)

```plain
cadastral_service/
├── app/            # Основное FastAPI-приложение
│   ├── alembic/      # Миграции базы данных
│   ├── api/          # API: роутеры, схемы, сервисы
│   ├── auth/         # Аутентификация и авторизация
│   ├── certs/        # RSA-ключи для JWT
│   ├── core/         # Конфигурация приложения
│   ├── tests/        # Pytest тесты
│   ├── main.py       # Точка входа приложения
│   └── ...           # Остальные файлы (.env, requirements и пр.)
│
├── external_app/   # Эмуляция внешнего сервиса
├── docker-compose.yml
└── README.md
```

✱ **Полная структура:** см. [PROJECTSTRUCTURE.md](PROJECTSTRUCTURE.md)

---

## Установка проекта

1. Клонируйте репозиторий
    ```shell
    git clone git@github.com:ZorinVS/cadastral_service.git \
        && cd cadastral_service
    ```
2. Подготовьте файл окружения
    ```sh
    cp app/.env.docker.example app/.env.docker \
       && nano app/.env.docker
   ```
3. Соберите Docker-образы
    ```sh
    docker-compose build
    ``` 

---


## Проверка работоспособности

1. Запустите контейнеры
    ```sh
    docker-compose up -d
    ```
2. Проверьте доступность сервиса
    - [GET /ping](http://localhost:8000/ping) — проверка доступности
    - [Swagger UI /docs](http://localhost:8000/docs) — документация API

---


## Тестирование

### Запуск тестов

```sh
docker-compose exec main_app pytest -v
```

### Покрытие

| File                                  | Class                      | Statements | Missing | Excluded | Coverage |
|---------------------------------------|-----------------------------|------------|---------|----------|----------|
| api/routers/query.py                  | (no class)                  | 36         | 14      | 0        | 61%      |
| tests/test_api_routers_query.py       | (no class)                  | 36         | 0       | 0        | 100%     |
| tests/test_api_services.py            | (no class)                  | 32         | 0       | 0        | 100%     |
| auth/deps.py                          | (no class)                  | 31         | 17      | 0        | 45%      |
| tests/conftest.py                     | (no class)                  | 31         | 0       | 0        | 100%     |
| auth/utils.py                         | (no class)                  | 28         | 13      | 0        | 54%      |
| core/config.py                        | (no class)                  | 25         | 0       | 0        | 100%     |
| tests/test_api_routers_checkhealth.py | (no class)                  | 22         | 0       | 0        | 100%     |
| api/schemas.py                        | (no class)                  | 21         | 0       | 0        | 100%     |
| auth/schemas.py                       | (no class)                  | 19         | 0       | 0        | 100%     |
| tests/test_api_utils.py               | (no class)                  | 19         | 0       | 0        | 100%     |
| auth/routers.py                       | (no class)                  | 18         | 8       | 0        | 56%      |
| main.py                               | (no class)                  | 15         | 3       | 0        | 80%      |
| tests/utils.py                        | (no class)                  | 14         | 0       | 0        | 100%     |
| tests/test_api_validators.py          | (no class)                  | 13         | 0       | 0        | 100%     |
| api/services.py                       | (no class)                  | 12         | 0       | 0        | 100%     |
| core/database.py                      | Database                    | 12         | 11      | 0        | 8%       |
| core/database.py                      | (no class)                  | 12         | 0       | 0        | 100%     |
| api/utils.py                          | (no class)                  | 11         | 0       | 0        | 100%     |
| api/routers/checkhealth.py            | (no class)                  | 10         | 0       | 0        | 100%     |
| api/validators.py                     | CadastralValidator          | 7          | 0       | 0        | 100%     |
| api/validators.py                     | (no class)                  | 6          | 0       | 0        | 100%     |
| core/deps.py                          | (no class)                  | 6          | 1       | 0        | 83%      |
| api/schemas.py                        | QueryRequestAddDTO          | 4          | 1       | 0        | 75%      |
| core/config.py                        | Settings                    | 3          | 2       | 0        | 33%      |
| api/exceptions.py                     | (no class)                  | 2          | 0       | 0        | 100%     |
| tests/utils.py                        | Dependency                  | 1          | 0       | 0        | 100%     |
| api/__init__.py                       | (no class)                  | 0          | 0       | 0        | 100%     |
| api/exceptions.py                     | ExternalServiceUnavailable  | 0          | 0       | 0        | 100%     |
| api/routers/__init__.py               | (no class)                  | 0          | 0       | 0        | 100%     |
| api/schemas.py                        | OrderBy                     | 0          | 0       | 0        | 100%     |
| api/schemas.py                        | QueryResponseDTO            | 0          | 0       | 0        | 100%     |
| api/schemas.py                        | QueryResponsesDTO           | 0          | 0       | 0        | 100%     |
| api/schemas.py                        | QueryHistoryResponseDTO     | 0          | 0       | 0        | 100%     |
| auth/__init__.py                      | (no class)                  | 0          | 0       | 0        | 100%     |
| auth/schemas.py                       | TokenInfo                   | 0          | 0       | 0        | 100%     |
| auth/schemas.py                       | UserDTO                     | 0          | 0       | 0        | 100%     |
| auth/schemas.py                       | UserRegisterDTO             | 0          | 0       | 0        | 100%     |
| auth/schemas.py                       | MessageResponse             | 0          | 0       | 0        | 100%     |
| core/__init__.py                      | (no class)                  | 0          | 0       | 0        | 100%     |
| core/config.py                        | JWTSettings                 | 0          | 0       | 0        | 100%     |
| tests/__init__.py                     | (no class)                  | 0          | 0       | 0        | 100%     |
| tests/conftest.py                     | CadastralData               | 0          | 0       | 0        | 100%     |
| **Total**                              |                             | **446**    | **70**  | **0**    | **84%**  |

---
