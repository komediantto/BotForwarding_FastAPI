# BotForwarding(FastAPI)

## Description

Customizable Telegram parser, with the ability to add any number of open channels for parsing. It can work in two modes:

   1. By default, it saves posts to the database for further editing. After confirming the change, sends the post to the target channel.
   2. Forwarding posts directly to the target channel, without saving them in the database and editing them

## Tech

FastAPI, Pyrogram, SQLAlchemy, PostgreSQL, alembic, dependency-injector, sqladmin, docker

## How to launch

Create an .env file in the root of the project of the form:

```env
API_ID = <your api_id>
API_HASH = <your api_hash>
DB_NAME = postgres
DB_USER = postgres
DB_PASS = postgres
DB_HOST = db
DB_PORT = 5432
```

From the root directory, run docker-compose

```bash
docker-compose up
```

At the first launch, you need to create a Pyrogram session, so go to the container

```bash
docker exec -it combined_app bash
```

Go to the api directory and run migrations

```bash
cd app/api
alembic upgrade head
```

Go to the client directory and run the script create_session.py

```bash
cd /BotForwarding/app/client
python create_session.py
```

After the message about the successful creation of the session, you will need to create a superuser, the script will offer to do this, enter the necessary data, create a superuser and run main.py:

```bash
cd /BotForwarding
python main.py
```

On subsequent launches of docker-compose (if any), you do not need to re-create the session, you can immediately start main.py .

The admin panel will be available at http://0.0.0.0:8000/admin .

For the application to work, you need to add a target channel (where posts will be sent) and channels for parsing, indicating the added target channel.

To switch the operating mode, there is a forwarding checkbox in the description of the target channel, activate it if you want to make a simple forwarding of posts without saving them to the database.

It is also possible to disable parsing for the target channel, to do this, uncheck the active checkbox.

## Screenshots

*authorization page*
![Снимок экрана от 2023-06-03 12-11-49](https://github.com/komediantto/BotForwarding_FastAPI/assets/62796239/006e805b-5285-4c95-9d03-eebfc7fc8dc9)

*user page*
![Снимок экрана от 2023-06-03 12-12-12](https://github.com/komediantto/BotForwarding_FastAPI/assets/62796239/ef9f752e-8083-4a6f-bfac-94d67f7fc0da)

*page with posts*
![Снимок экрана от 2023-06-03 12-12-53](https://github.com/komediantto/BotForwarding_FastAPI/assets/62796239/824d85b4-9063-43b7-b0db-8c1e690cf82b)

*page with target channels*
![Снимок экрана от 2023-06-03 12-13-32](https://github.com/komediantto/BotForwarding_FastAPI/assets/62796239/061f5d75-8843-4473-b79b-d78a93ab0b14)

*page with channels for parsing*
![Снимок экрана от 2023-06-03 12-13-43](https://github.com/komediantto/BotForwarding_FastAPI/assets/62796239/09e0df55-d4d7-4474-92c9-2af6b8ac3abb)

*page with media files*
![Снимок экрана от 2023-06-03 12-14-02](https://github.com/komediantto/BotForwarding_FastAPI/assets/62796239/6da833b1-d478-4dda-a02e-1b83ff1520f4)

## Note

*During development, we had to change the sqladmin library files a little, the modified files are in the sqladmin_patch folder and automatically replace the original files when deploying containers.*
