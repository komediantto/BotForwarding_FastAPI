from markupsafe import Markup
from sqladmin import ModelView

from .models import Channel, MediaFile, Post, Target
from .tools import get_media_list, get_target_telegram_id, send_message


class TargetAdmin(ModelView, model=Target):
    '''Отображение страницы целевых каналов'''
    column_list = ['telegram_id', 'name', 'channels', 'posts']
    column_formatters = {
        'posts': lambda target, a: [
            Markup(f'{str(post)}</br>') for post in target.posts
            ],
        'channels': lambda target, a: [
            Markup(f'{str(channel)}</br>') for channel in target.channels
        ]
    }


class ChannelAdmin(ModelView, model=Channel):
    '''Отображение каналов для парсинга'''
    column_list = ['telegram_id', 'name']


class PostAdmin(ModelView, model=Post):
    '''Отображение страницы постов'''
    column_list = ['id', 'text', 'mediafiles']
    column_labels = {"id": "ID",
                     "text": "Текст сообщения",
                     "mediafiles": "Медиафайлы"}

    '''Здесь настраивается отображение медиафайлов в столбик, по умолчанию идёт в строчку
     P.S. пришлось лезть в кишки sqladmin чтобы убрать скобки вокруг связанных объектов
     ''' # noqa

    column_formatters = {
        'mediafiles': lambda post, a: [
            Markup(f'{str(media)}</br>') for media in post.mediafiles]
    }
    column_formatters_detail = {
        'mediafiles': lambda post, a: [
            Markup(f'{str(media)}</br>') for media in post.mediafiles]
    }

    async def after_model_change(self, data, model, is_created):
        '''Отправка поста в целевой канал после установки флага is_verified'''
        media_list = get_media_list(data['mediafiles'])
        target_id = get_target_telegram_id(data['target'])
        text = data['text']
        if data['is_verified'] is True:
            await send_message(int(target_id), text, media_list)


class MediaAdmin(ModelView, model=MediaFile):
    '''Отображение страницы медиафайлов'''
    column_list = ['url', 'post_id']
    column_details_list = ['post', 'url']
    column_formatters = {
        'url': lambda media, a: Markup(
            f'<a href="{media.url}" target="_blank">Посмотреть медиафайл</a>')
    }
    column_formatters_detail = {
        'url': lambda media, a: Markup(
            f'<a href="{media.url}" target="_blank">Посмотреть медиафайл</a>')
    }
