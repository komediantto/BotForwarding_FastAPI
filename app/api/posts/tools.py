from typing import List

from dependency_injector.wiring import Provide, inject
from loguru import logger
from pyrogram.client import Client
from pyrogram.types import InputMediaPhoto, InputMediaVideo

from app.api.posts.models import Target
from app.core.container import Container
from app.core.settings import settings
from app.db.service.media_service import MediaService
from app.db.service.target_service import TargetService

from .exceptions import InvalidTargetId, MediaFileError


async def send_message(telegram_id: int, text: str, media_list: List[str]):
    '''Отправка сообщения в целевой канал'''
    async with Client('fast_client',
                      settings.API_ID, settings.API_HASH) as client:
        if len(media_list) > 1:
            await create_and_send_media_group(media_list, text,
                                              client, telegram_id)
        elif len(media_list) == 1:
            await send_single_file(media_list, text, client, telegram_id)
        else:
            await client.send_message(telegram_id, text)


async def create_and_send_media_group(media_list: List[str], text: str,
                                      client: Client, telegram_id: int):
    '''Создание и отправление медиагруппы с caption'''
    input_files = []
    for i, media in enumerate(media_list):
        if get_media_type(media) == 'image':
            if i == 0:
                input_files.append(
                    InputMediaPhoto(f'../media/{media}',
                                    caption=text))
            else:
                input_files.append(
                    InputMediaPhoto(f'../media/{media}'))
        elif get_media_type(media) == 'video':
            if i == 0:
                input_files.append(
                    InputMediaVideo(f'../media/{media}', caption=text))
            else:
                input_files.append(
                    InputMediaVideo(f'../media/{media}'))
    await client.send_media_group(telegram_id, input_files)
    logger.debug('Отправлено')


async def send_single_file(media_list: List[str], text: str,
                           client: Client, telegram_id: int):
    '''Отправка одиночного файла с caption'''
    if get_media_type(media_list[0]) == 'image':
        await client.send_photo(
            telegram_id,
            f'app/media/{media_list[0]}',
            text)
    elif get_media_type(media_list[0]) == 'video':
        await client.send_video(
            telegram_id, f'app/media/{media_list[0]}', text)


def get_media_type(file_name: str):
    if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
        return 'image'
    elif file_name.lower().endswith(('.mp4', '.mkv')):
        return 'video'
    else:
        return None


@inject
def get_media_list(media_ids: List[int],
                   media_service: MediaService = Provide[
                       Container.media_service]) -> List[str]:
    '''Получение списка имён файлов для создания телеграм объектов'''
    media_list = []
    for media_id in media_ids:
        media = media_service.get(media_id)
        if media:
            media_list.append(str(media))
        else:
            raise MediaFileError
    return media_list


@inject
def get_target_telegram_id(target_id: int,
                           target_service: TargetService = Provide[
                               Container.target_service]) -> int:
    '''Получение айдишника целевого канала'''
    target: Target = target_service.get(target_id)
    if target:
        telegram_id = target.telegram_id
    else:
        raise InvalidTargetId
    return telegram_id
