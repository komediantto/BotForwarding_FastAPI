from dependency_injector.wiring import Provide, inject
from loguru import logger

from app.core.container import Container
from app.db.service.session_service import SessionService


@inject
def get_session_string(
        session_service: SessionService = Provide[Container.session_service]):
    logger.warning(session_service)
    session = session_service.get(id=1)
    session_string = session.session_string
    return session_string
