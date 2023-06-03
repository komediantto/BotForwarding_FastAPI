from app.db.repository.media import RepositoryMedia


class MediaService:

    def __init__(self, repository_media: RepositoryMedia):
        self._repository_media = repository_media

    def get(self, id):
        return self._repository_media.get(id=id)

    def create(self, obj_in: dict):
        return self._repository_media.create(
            obj_in=obj_in,
            commit=True
        )
