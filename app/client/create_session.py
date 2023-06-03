from datetime import date

from loguru import logger
from pyrogram.client import Client

from app.api.users.admin import pwd_context
from app.api.users.models import User
from app.client.models import TgSession
from app.core.settings import settings
from app.db.session import SyncSession

api_id = settings.API_ID
api_hash = settings.API_HASH


def create_pyrogram_session():
    create = input('Создать новую сессию?(д/Н): ')
    if create.lower() in ('д', 'y'):
        session = SyncSession(settings.SYNC_SQLALCHEMY_DATABASE_URI)
        with Client("pyroclient", api_id,
                    api_hash, in_memory=True) as client:
            session_string = client.export_session_string()
            tg_session = TgSession(session_string=session_string)
        session.session.add(tg_session)
        session.session.commit()
        logger.info('Сессия успешно создана.')
    else:
        return


def create_super_user():
    create = input('Создать нового админа?(д/Н): ')
    if create.lower() in ('д', 'y'):
        username = input('Введите логин(username): ')
        email = input('Введите email: ')
        password = input('Введите пароль: ')
        hashed_password = pwd_context.hash(password)
        session = SyncSession(settings.SYNC_SQLALCHEMY_DATABASE_URI)
        admin = User(username=username,
                     email=email,
                     password=hashed_password,
                     created=date.today(),
                     is_active=True)
        session.session.add(admin)
        session.session.commit()
        logger.info('Администратор успешно создан')
    else:
        return


if __name__ == '__main__':
    create_pyrogram_session()
    create_super_user()
