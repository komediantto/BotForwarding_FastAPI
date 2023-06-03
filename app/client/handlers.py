from typing import List

from loguru import logger
from pyrogram import types
from pyrogram.client import Client

from app.api.posts.models import Target
from app.client.interface import interface
from app.client.utils import create_data_for_api, get_channels, send_to_channel

media_group_chats = set()


async def post_handler(client: Client, message: types.Message):
    '''Ловим сообщения без прикреплений, либо с одним прикреплением'''
    target_channels: List[Target] = get_channels()
    for target in target_channels:
        if message.chat.id in \
           [int(channel.telegram_id) for channel in target.channels]:
            if target.forwarding:
                await send_to_channel(client, message, target)
            else:
                data = await create_data_for_api(message, client, target)
                if interface.create_post(data=data):
                    logger.debug('Успех')
                else:
                    logger.debug('Провал')


async def media_group_handler(client: Client, message: types.Message):
    '''Ловим медиагруппы'''
    target_channels = get_channels()
    channels = []
    for target in target_channels:
        channels += [int(channel.telegram_id) for channel in target.channels]

    if message.chat.id not in channels or message.chat.id in media_group_chats:
        return

    media_group_chats.add(message.chat.id)

    for target in target_channels:
        if target.forwarding:
            await send_to_channel(client, message, target, media_group=True)

        else:
            data = await create_data_for_api(message, client,
                                             target, media_group=True)
            if interface.create_post(data=data):
                logger.warning('Успех')
            else:
                logger.warning('Провал')
        media_group_chats.clear()
