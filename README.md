# BotForwarding(FastAPI)

## Описание

Настраиваемый парсер Telegram, с возможностью добавления любого количества открытых каналов для парсинга. Может работать в двух режимах:

   1. По умолчанию сохраняет посты в базу данных для дальнейшего редактирования. После подтверждения изменения отправляет пост в целевой канал.
   2. Пересылка постов напрямую в целевой канал, без сохранения в БД и возможности редактирования

## Технологии

FastAPI, Pyrogram, SQLAlchemy, PostgreSQL, alembic, dependency-injector, sqladmin, docker

## Как запустить

Создать .env файл в корне проекта вида:

```env
API_ID = <свой api_id>
API_HASH = <свой api_hash>
DB_NAME = postgres
DB_USER = postgres
DB_PASS = postgres
DB_HOST = db
DB_PORT = 5432
```

Из корневой директории запустить docker-compose

```bash
docker-compose up
```

При первом запуске требуется создать сессию Pyrogram, так что идём в контейнер

```bash
docker exec -it combined_app bash
```

Переходим в директорию api и накатываем миграции

```bash
cd app/api
alembic upgrade head
```

Переходим в директорию client и запускаем скрипт create_session.py

```bash
cd /BotForwarding/app/client
python create_session.py
```

После сообщения об успешном создании сессии потребуется создать суперюзера, скрипт предложит это сделать, вводим необходимые данные, создаём суперюзера и запускаем main.py:

```bash
cd /BotForwarding
python main.py
```

При последующих запусках docker-compose(если таковые будут) не нужно заново создавать сессию, можно сразу запускать main.py.

Админка будет доступна по адресу http://0.0.0.0:8000/admin.

Для работы приложения нужно добавить целевой канал(куда будут отправляться посты) и каналы для парсинга, с указанием добавленного целевого канала.

Для переключения режима работы в описании целевого канала есть флажок forwarding, активируйте его, если хотите сделать простую пересылку постов без сохранения в БД.

Также есть возможность выключить парсинг для целевого канала, для этого нужно снять флажок active.

## Скриншоты

*страница авторизации*
![Снимок экрана от 2023-06-03 12-11-49](https://github.com/komediantto/BotForwarding_FastAPI/assets/62796239/006e805b-5285-4c95-9d03-eebfc7fc8dc9)

*страница с пользователями*
![Снимок экрана от 2023-06-03 12-12-12](https://github.com/komediantto/BotForwarding_FastAPI/assets/62796239/ef9f752e-8083-4a6f-bfac-94d67f7fc0da)

*страница с постами*
![Снимок экрана от 2023-06-03 12-12-53](https://github.com/komediantto/BotForwarding_FastAPI/assets/62796239/824d85b4-9063-43b7-b0db-8c1e690cf82b)

*страница с целевыми каналами*
![Снимок экрана от 2023-06-03 12-13-32](https://github.com/komediantto/BotForwarding_FastAPI/assets/62796239/061f5d75-8843-4473-b79b-d78a93ab0b14)

*страница с каналами для парсинга*
![Снимок экрана от 2023-06-03 12-13-43](https://github.com/komediantto/BotForwarding_FastAPI/assets/62796239/09e0df55-d4d7-4474-92c9-2af6b8ac3abb)

*страница с медиафайлами*
![Снимок экрана от 2023-06-03 12-14-02](https://github.com/komediantto/BotForwarding_FastAPI/assets/62796239/6da833b1-d478-4dda-a02e-1b83ff1520f4)

>[!info] Примечание
>*Во время разработки пришлось немного изменить файлы библиотеки sqladmin, изменённые файлы лежат в папке sqladmin_patch и автоматически заменяют оригинальные файлы при развёртывании контейнеров.*
