from typing import List
from app.db.repository.target import RepositoryTarget
from app.api.posts.models import Target


class TargetService:

    def __init__(self, repository_target: RepositoryTarget):
        self._repository_target = repository_target

    def get(self, id):
        return self._repository_target.get(id=id)

    def create(self, obj_in: dict):
        return self._repository_target.create(
            obj_in=obj_in,
            commit=True
        )

    def get_all(self) -> List[Target]:
        return self._repository_target.list()
