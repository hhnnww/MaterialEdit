import re
from hashlib import sha256
from typing import Generator, List

from module_素材采集.core.class_htmldown import HTMLDown
from module_素材采集.core.model import MaterialType


class ChaoPX:
    def __init__(self, start_url: str, max_page: int, cookie: str = ''):
        self.start_url = start_url
        self.max_page = max_page
        self.cookie = cookie

    def fun_构建列表页(self):
        last_path = self.start_url.split('/')
        num_path = last_path[-1].split('-')

        for x in range(1, self.max_page):
            num_path[-2] = str(x)
            new_num_path = '-'.join(num_path)

            last_path[-1] = new_num_path
            new_path = '/'.join(last_path)

            yield new_path

    def fun_单页获取素材(self, url: str):
        html = HTMLDown(url, cookie=self.cookie).html
