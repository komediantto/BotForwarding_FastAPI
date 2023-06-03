from typing import Any
from app.db.repository.session import RepositorySession


class SessionService:

    def __init__(self, repository_session: RepositorySession):
        self._repository_session = repository_session

    async def get_or_create(self, obj_in: Any):
        if isinstance(obj_in, dict):
            session = self._repository_session.get(id=int(obj_in.get("id")))
            if session is not None:
                return session
            return self._repository_session.create(obj_in=obj_in, commit=True)

    def get(self, id):
        return self._repository_session.get(id=id)
