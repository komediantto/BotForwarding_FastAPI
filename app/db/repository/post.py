from .base import RepositoryBase
from app.api.posts.models import Post


class RepositoryPost(RepositoryBase[Post]):
    pass
