import requests
from loguru import logger


class Interface:
    posts_url = "http://localhost:8000/posts/"

    def create_post(self, data):
        '''Отправка запроса к апи на создание поста'''
        response = requests.post(self.posts_url, json=data)
        try:
            logger.warning(response.json())
        except requests.exceptions.JSONDecodeError as e:
            logger.warning(f"JSONDecodeError: {e}")
            return False

        if response.status_code == 200 or response.status_code == 201:
            return True


interface = Interface()
