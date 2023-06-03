from typing import List, Optional, Union

from dependency_injector.wiring import Provide, inject
from loguru import logger
from pyrogram import types
from pyrogram.client import Client

from app.api.posts.models import Target
from app.client.exceptions import EmptyTargetError
from app.core.container import Container
from app.db.service.target_service import TargetService


@inject
def get_channels(target: TargetService = Provide[Container.target_service]) \
                                                    -> List[Target]:
    '''Получение таргет-каналов'''
    target_channels = target.get_all()
    if target_channels is None:
        raise EmptyTargetError

    return target_channels


def generate_telegram_files(media_messages: List[types.Message]) -> \
                                List[Union[types.InputMediaPhoto,
                                           types.InputMediaVideo]]:
    '''Генерирует список из телеграм файлов'''
    media_list = []
    for media in media_messages:
        if media.photo:
            if media.caption:
                media_list.append(
                    types.InputMediaPhoto(media.photo.file_id,
                                          caption=media.caption.markdown))
            else:
                media_list.append(types.InputMediaPhoto(media.photo.file_id))
        elif media.video:
            if media.caption:
                media_list.append(
                    types.InputMediaVideo(media.video.file_id,
                                          caption=media.caption.markdown))
            else:
                media_list.append(types.InputMediaVideo(media.video.file_id))
    return media_list


async def send_only_one_attachment(client: Client,
                                   message: types.Message,
                                   target: Target) -> None:
    '''Отправляет пустое сообщение, либо сообщение с одним файлом'''
    if message.photo:
        try:
            await client.send_photo(chat_id=int(target.telegram_id),
                                    photo=message.photo.file_id,
                                    caption=message.caption.markdown)
        except AttributeError:
            await client.send_photo(chat_id=int(target.telegram_id),
                                    photo=message.photo.file_id)
    elif message.video:
        await client.send_video(chat_id=int(target.telegram_id),
                                video=message.video.file_id,
                                caption=message.caption.markdown)
    else:
        await client.send_message(chat_id=int(target.telegram_id),
                                  text=message.text.markdown)


async def send_to_channel(client: Client,
                          message: types.Message, target: Target,
                          media_group=False):
    '''Пересылка сообщения в таргет-канал'''
    if media_group:
        media_group_messages = await client.get_media_group(
            chat_id=message.chat.id,
            message_id=message.id)
        media = generate_telegram_files(media_group_messages)
        await client.send_media_group(chat_id=int(target.telegram_id),
                                      media=media)
    else:
        await send_only_one_attachment(client, message, target)


async def create_data_for_api(message: types.Message,
                              client: Client, target: Target,
                              media_group=False):
    files: List[str] = list()
    text: Optional[str] = None
    if media_group:
        data = await with_media_group(client, message, target, files)
    else:
        if message.photo or message.video:
            media = await client.download_media(message, 'app/media/')
            files.append(media)
        if message.caption:
            text = message.caption.markdown if hasattr(
                message.caption, 'markdown') else None
        elif message.text:
            text = message.text.markdown if hasattr(
                message.text, 'markdown') else None
        data = {
            'text': text,
            'mediafiles': files,
            'target': target.id
                    }
    return data


async def with_media_group(client: Client, message: types.Message,
                           target: Target, files: list):
    media_group_messages = await client.get_media_group(
        chat_id=message.chat.id, message_id=message.id)
    for media_message in media_group_messages:
        media = await client.download_media(media_message,
                                            'app/media/')
        files.append(media)
        if media_message.caption:
            text = media_message.caption.markdown

    data = {'text': text,
            'mediafiles': files,
            'target': target.id
            }
    logger.warning(data)
    return data
