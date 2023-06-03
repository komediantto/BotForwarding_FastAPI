from dependency_injector import containers, providers

from app.api.posts.models import MediaFile, Post, Target
from app.api.users.models import User
from app.client.models import TgSession
from app.core.settings import Settings
from app.db.repository.media import RepositoryMedia
from app.db.repository.post import RepositoryPost
from app.db.repository.session import RepositorySession
from app.db.repository.target import RepositoryTarget
from app.db.repository.user import RepositoryUser
from app.db.service.media_service import MediaService
from app.db.service.post_service import PostService
from app.db.service.session_service import SessionService
from app.db.service.target_service import TargetService
from app.db.service.user_service import UserService
from app.db.session import SyncSession


class Container(containers.DeclarativeContainer):

    config = providers.Singleton(Settings)
    db = providers.Singleton(SyncSession,
                             db_url=config.provided.SYNC_SQLALCHEMY_DATABASE_URI)

    repository_target = providers.Singleton(RepositoryTarget,
                                            model=Target, session=db)
    repository_post = providers.Singleton(RepositoryPost,
                                          model=Post, session=db)
    repository_media = providers.Singleton(RepositoryMedia,
                                           model=MediaFile, session=db)
    repository_user = providers.Singleton(RepositoryUser,
                                          model=User, session=db)
    repository_session = providers.Singleton(RepositorySession,
                                             model=TgSession, session=db)

    target_service = providers.Singleton(
        TargetService,
        repository_target=repository_target
    )
    post_service = providers.Singleton(
        PostService,
        repository_post=repository_post,
    )
    media_service = providers.Singleton(
        MediaService,
        repository_media=repository_media
    )
    user_service = providers.Singleton(
        UserService,
        repository_user=repository_user
    )
    session_service = providers.Singleton(
        SessionService,
        repository_session=repository_session
    )
