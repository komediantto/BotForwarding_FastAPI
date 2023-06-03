from app.db.repository.post import RepositoryPost


class PostService:

    def __init__(self, repository_post: RepositoryPost):
        self._repository_post = repository_post

    async def create(self, obj_in: dict):
        return self._repository_post.create(
            obj_in=obj_in,
            commit=True
        )

    def get_all(self):
        return self._repository_post.list()
