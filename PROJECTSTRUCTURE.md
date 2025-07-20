# Структура проекта

```plain
cadastral_service/
├── app/                      # Основное приложение FastAPI
│   ├── alembic/                # Миграции базы данных (Alembic)
│   │   ├── versions/             # Миграции для создания таблиц `queries` и `users`
│   │   ├── env.py
│   │   └── script.py.mako
│   │
│   ├── api/                    # API: роутеры, схемы, сервисы, валидация
│   │   ├── routers/              # Роутеры FastAPI
│   │   │   ├── __init__.py
│   │   │   ├── checkhealth.py    # `/ping` эндпоинт
│   │   │   └── query.py          # `/query`, `/history` эндпоинты
│   │   ├── __init__.py
│   │   ├── exceptions.py         # Обработка ошибок API
│   │   ├── schemas.py            # Pydantic-схемы запросов и ответов
│   │   ├── services.py           # Логика работы с БД и внешним сервисом
│   │   ├── utils.py              # Утилиты общего назначения
│   │   └── validators.py         # Пользовательская валидация данных
│   │
│   ├── auth/                   # Регистрация, авторизация, токены
│   │   ├── __init__.py
│   │   ├── deps.py               # Depends-зависимости для авторизации
│   │   ├── routers.py            # Эндпоинты регистрации / аутентификации
│   │   ├── schemas.py            # Pydantic-схемы авторизации
│   │   └── utils.py              # Генерация токенов, хеширование паролей
│   │
│   ├── certs/                  # RSA-ключи для JWT (генерируются автоматически при работе с контейнерами)
│   │   ├── private.pem
│   │   └── public.pem
│   │
│   ├── core/                   # Конфигурация приложения и базы данных
│   │   ├── __init__.py
│   │   ├── config.py             # Настройки из .env файлов
│   │   ├── database.py           # Подключение к PostgreSQL (asyncpg)
│   │   └── deps.py               # Depends для базы данных
│   │
│   ├── tests/                  # Тесты Pytest
│   │   ├── __init__.py
│   │   ├── conftest.py           # Фикстуры для тестов
│   │   ├── test_api_routers_checkhealth.py
│   │   ├── test_api_routers_query.py
│   │   ├── test_api_services.py
│   │   ├── test_api_validators.py
│   │   └── utils.py
│   │
│   ├── .env                    # Локальная конфигурация среды
│   ├── .env.docker             # Конфигурация среды для Docker
│   ├── Dockerfile              # Dockerfile основного приложения
│   ├── htmlcov/                # Отчет покрытия тестами (pytest --cov)
│   ├── main.py                 # Точка входа FastAPI приложения
│   ├── requirements.txt        # Зависимости приложения
│   ├── sample.env              # Пример .env файла
│   └── sample.env.docker       # Пример .env файла для Docker
│
├── external_app/               # Эмуляция внешнего сервиса (отдельный FastAPI)
│   ├── Dockerfile                # Dockerfile для эмулятора внешнего сервиса
│   ├── main.py                   # Точка входа внешнего сервиса
│   ├── requirements.txt          # Зависимости внешнего сервиса
│   └── schemas.py                # Pydantic-схемы внешнего сервиса
│
├── docker-compose.yml            # Docker Compose для сборки и запуска сервисов
└── README.md                     # Документация проекта
```
