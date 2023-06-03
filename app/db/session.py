from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from contextvars import ContextVar

scope: ContextVar = ContextVar('db_session_scope')


def scopefunc():
    try:
        return scope.get()
    except LookupError:
        print("scope not set")


class SyncSession:

    def __init__(self, db_url: str, dispose_session: bool = False):
        self.db_url = db_url
        self.dispose_session = dispose_session
        self.sync_engine = create_engine(self.db_url,
                                         pool_pre_ping=True,
                                         echo=True)
        self.sync_session_factory = sessionmaker(bind=self.sync_engine,
                                                 autoflush=False,
                                                 expire_on_commit=False)
        self.scoped_session = scoped_session(self.sync_session_factory,
                                             scopefunc=scopefunc)
        self.session = self.scoped_session()

    def get_engine(self):
        return self.sync_engine
