# TestWork24 - Quotes Scraper Service

Веб-сервис для парсинга цитат с сайта https://quotes.toscrape.com/ с использованием FastAPI, Celery, Redis и MongoDB.

## Технологии

- **FastAPI** - веб-фреймворк
- **MongoDB** - база данных
- **Poetry** - управление зависимостями
- **Docker & Docker Compose** - контейнеризация
- **Celery** - очередь задач
- **Redis** - брокер сообщений
- **BeautifulSoup** - парсинг HTML

## Структура проекта

```
TestWork24/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI приложение
│   ├── routers.py       # Маршруты API
|   |── config.py        # Конфигурация приложения
|   |── schemas.py       # Pydantic схемы
│   ├── tasks.py         # Celery задачи
│   ├── database.py      # Подключение к MongoDB
│   ├── models.py        # Pydantic модели
│   └── scraper.py       # Логика парсинга
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── poetry.lock
├── .env.example
├── .env
└── README.md
```

## Запуск проекта

### Вариант 1: С использованием Docker Compose (рекомендуется)

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/BahaGit2002/TestWork24
   cd TestWork24
   ```

2. **Создайте .env файл из примера:**
   ```bash
      cp .env.example .env
   ```
   
3. **Запустите проект:**
    ```bash
    docker-compose up --build
    ```

Готово! Приложение доступно по адресу http://localhost:8000


### Вариант 2: Локальный запуск

1. **Установите зависимости:**
   ```bash
   # Установите Poetry (если не установлен)
   curl -sSL https://install.python-poetry.org | python3 -
   
   # Установите зависимости проекта
   poetry install
   ```

2. **Настройте переменные окружения:**
   ```bash
   cp .env_example .env
   ```

   Отредактируйте `.env` файл:
   ```env
   MONGODB_URL=mongodb://mongo:27017/quotes_db
    REDIS_URL=redis://redis:6379/0
    CELERY_BROKER_URL=redis://redis:6379/0
    CELERY_RESULT_BACKEND=redis://redis:6379/0
   ```

3. **Запустите Redis и MongoDB через Docker::**
   ```bash
   # Используя Docker
    docker run -d --name redis -p 6379:6379 redis:6.2
    docker run -d --name mongo -p 27017:27017 -v mongo_data:/data/db mongo:5.0
   ```

4. **Запустите приложение:**
   ```bash
   poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

5. **Запустите Celery воркер в отдельном терминале:**
   ```bash
   poetry run celery -A app.tasks worker --loglevel=info
   ```

Готово! Приложение доступно по адресу http://localhost:8000

## API Endpoints

### Аутентификация
- `POST /parse-quotes-task` - Запускает асинхронную задачу парсинга цитат.
- `GET /quotes` - Получает цитаты из базы данных с возможностью фильтрации.

## Документация API

После запуска приложения документация доступна по адресам:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Переменные окружения

| Переменная              | Описание                                  | Значение по умолчанию |
|-------------------------|-------------------------------------------|-----------------------|
| `MONGODB_URL`           | URL подключения к MongoDB                 | -                     |
| `REDIS_URL`             | URL подключения к Redis                   | -                     |
| `CELERY_BROKER_URL`     | URL брокера сообщений для Celery          | -                     |
| `CELERY_RESULT_BACKEND` | URL для хранения результатов задач Celery | -                     |


## 📝 Логирование
Все компоненты настроены на подробное логирование:

**FastAPI:** Логи запросов и ошибок
**Celery:** Логи выполнения задач
**Scraper:** Логи процесса парсинга и сохранения

Логи доступны через 
``` bash
docker-compose logs <service_name>.
```

## 🔧 Дальнейшее развитие

## Возможные улучшения:

- Добавление тестов (pytest)
- Реализация Celery Flower для мониторинга задач
- Добавление rate limiting
- Кэширование частых запросов
- Метрики и мониторинг (Prometheus/Grafana)
- CI/CD pipeline
