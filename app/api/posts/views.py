from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from loguru import logger

from app.core.container import Container
from app.db.service.media_service import MediaService
from app.db.service.post_service import PostService

from .schemas import PostCreate

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.post('/')
@inject
async def create_post(new_post: PostCreate,
                      post_service: PostService = Depends(Provide[
                          Container.post_service]),
                      media_service: MediaService = Depends(Provide[
                          Container.media_service])):
    logger.warning(post_service)
    post = await post_service.create({'text': new_post.text,
                                      'target_channel_id': new_post.target})
    logger.warning(post)
    if new_post.mediafiles:
        for media in new_post.mediafiles:
            file_name = media.split('/')[-1]
            url = f'http://127.0.0.1:8000/media/{file_name}'
            media_service.create(obj_in={'path': media,
                                         'url': url,
                                         'post_id': post.id})

    return {"result": post}
