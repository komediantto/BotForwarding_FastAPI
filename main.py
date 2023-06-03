import multiprocessing

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from loguru import logger
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from sqladmin import Admin

from app.api.posts import tools, views
from app.api.posts.admin import (ChannelAdmin, MediaAdmin, PostAdmin,
                                 TargetAdmin)
from app.api.posts.views import router as router_post
from app.api.users import admin as admin_module
from app.api.users import authentication
from app.api.users.admin import UserAdmin
from app.api.users.authentication import AdminAuth
from app.client import config as cfg
from app.client import handlers, utils
from app.client.handlers import media_group_handler, post_handler
from app.core.container import Container

# ***********Настройка контейнера*****************
container = Container()
db = container.db()
container.wire(modules=[cfg, handlers, utils,
                        views, admin_module, tools,
                        authentication])
# ************************************************


# **********Настройка Pyrogram********************
session_string = cfg.get_session_string()

client = Client('pyroclient', session_string=session_string)
client.add_handler(MessageHandler(post_handler, filters=(filters.channel) & ~(filters.media_group)))
client.add_handler(MessageHandler(media_group_handler, filters=[filters.channel, filters.media_group]))
# ************************************************


# **********Настройка FastAPI*********************
class MyApp(FastAPI):

    def create_admin(self, engine, auth):
        admin = Admin(self, engine, authentication_backend=auth)
        return admin


myapp = MyApp(title="Bot Forwarding")

myapp.include_router(router_post)
myapp.mount("/media", StaticFiles(directory="app/media"), name="media")
# *************************************************


# **********Настройка админки**********************
authentication_backend = AdminAuth(secret_key="...")


admin = myapp.create_admin(db.get_engine(), authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(PostAdmin)
admin.add_view(TargetAdmin)
admin.add_view(ChannelAdmin)
admin.add_view(MediaAdmin)
# *************************************************


def run_pyrogram():
    client.run()


def run_fastapi():
    uvicorn.run(myapp, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    pyrogram_process = multiprocessing.Process(target=run_pyrogram)
    fastapi_process = multiprocessing.Process(target=run_fastapi)

    pyrogram_process.start()
    logger.info('Процесс Pyrogram запущен')
    fastapi_process.start()
    logger.info('Процесс FastAPI запущен')

    pyrogram_process.join()
    fastapi_process.join()
