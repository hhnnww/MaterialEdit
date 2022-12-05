import re
from hashlib import sha256
from typing import Generator, List

from module_素材采集.core.class_htmldown import HTMLDown
from module_素材采集.core.model import MaterialType
from urllib.parse import urlparse, parse_qs


class SCFreePik:
    def __init__(self, start_url: str, max_page: int, cookie: str = ''):
        self.start_url = start_url
        self.max_page = max_page
        self.cookie = cookie

    def fun_构建列表(self):
        url_parse = urlparse(self.start_url)
        url_dict = parse_qs(url_parse.query)
        url_dict['sort'] = ['recent']

        for x in range(1, self.max_page + 1):
            url_dict['page'] = [str(x)]
            ori_query = '?'
            for item in url_dict.items():
                ori_query += f'{item[0]}={item[1][0]}&'

            ori_url = f'{url_parse.scheme}://{url_parse.netloc}{url_parse.path}{ori_query}'
            yield ori_url

    def fun_获取单页内素材(self, url):
        html = HTMLDown(url, cookie=self.cookie).html
        ma_list = html.find('#main > div.list-view > div > div.list-content > section > div > figure.caption')
        for ma in ma_list:
            url: str = ma.find('a', first=True).attrs.get('href')
            img: str = ma.attrs.get('data-image')

            yield MaterialType(url=url, img=img, hash=sha256(url.encode('utf-8')).hexdigest())

    def main(self):
        for page in self.fun_构建列表():
            for ma_obj in self.fun_获取单页内素材(page):
                yield ma_obj
