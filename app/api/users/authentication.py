from typing import NamedTuple, Optional

from dependency_injector.wiring import Provide, inject
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.api.users.admin import pwd_context
from app.core.container import Container
from app.db.service.user_service import UserService


class Verification(NamedTuple):
    allowed: bool
    error: Optional[str] = None


'''Пришлось внести изменения в библиотеку sqladmin, файлы application.py и
login.html, чтобы ошибкой подсвечивалось именно то поле, в котором пользователь
совершил ошибку. Теперь функция логин возвращает NamedTuple со статусом
верификации и текстом ошибки'''


class AdminAuth(AuthenticationBackend):

    @inject
    async def login(self, request: Request,
                    user_service: UserService = Provide[
                        Container.user_service]) -> Verification:
        form = await request.form()
        username = form.get('username')
        password = form.get('password')

        if not username:
            error = Verification(False, 'username')
            return error
        elif not password:
            error = Verification(False, 'password')
            return error

        user = user_service.get(username=username)
        if user is None:
            error = Verification(False, 'username')
            return error
        stored_password = user.password

        is_password_valid = pwd_context.verify(password, stored_password)

        if not is_password_valid:
            error = Verification(False, 'password')
            return error
        request.session.update({"token": "..."})
        ok = Verification(True)
        return ok

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self,
                           request: Request) -> Optional[RedirectResponse]:
        token = request.session.get("token")

        if not token:
            return RedirectResponse(request.url_for("admin:login"),
                                    status_code=302)
