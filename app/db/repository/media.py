from .base import RepositoryBase
from app.api.posts.models import MediaFile


class RepositoryMedia(RepositoryBase[MediaFile]):
    pass
