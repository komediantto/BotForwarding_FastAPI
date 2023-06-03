from typing import List
from app.db.repository.user import RepositoryUser
from app.api.users.models import User


class UserService:

    def __init__(self, repository_user: RepositoryUser):
        self._repository_user = repository_user

    def get(self, id=None, username=None):
        if username is not None:
            return self._repository_user.get(username=username)
        return self._repository_user.get(id=id)

    def create(self, obj_in: dict):
        return self._repository_user.create(
            obj_in=obj_in,
            commit=True
        )

    def update(self, user_id: int, obj_in: dict):
        return self._repository_user.update(
            db_obj=self._repository_user.get(id=user_id),
            obj_in=obj_in,
            commit=True
        )

    def get_all(self) -> List[User]:
        return self._repository_user.list()
