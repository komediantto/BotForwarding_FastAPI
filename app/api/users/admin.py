from dependency_injector.wiring import Provide, inject
from loguru import logger
from passlib.context import CryptContext
from sqladmin import ModelView

from app.core.container import Container
from app.db.service.user_service import UserService

from .models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.email, User.is_active]

    @inject
    async def after_model_change(self, data, model, is_created,
                                 user: UserService = Provide[
                                     Container.user_service]):
        '''Хэширование введённого пароля'''
        logger.warning(is_created)
        password = data['password']
        hashed_password = pwd_context.hash(password)
        user.update(model.id, {'password': hashed_password})
