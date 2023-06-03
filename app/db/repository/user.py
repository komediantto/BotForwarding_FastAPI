from .base import RepositoryBase
from app.api.users.models import User


class RepositoryUser(RepositoryBase[User]):
    pass
