import json
import re
from functools import cached_property
from hashlib import sha256

from module_素材采集.core.class_htmldown import HTMLDown
from module_素材采集.core.model import MaterialType


class SCPngTree:
    def __init__(self, start_url: str, max_page: int, cookie: str = ''):

        self.url = start_url
        self.max_page = max_page
        self.cookie = cookie

    @cached_property
    def __get_keyword(self):
        url_split = self.url.split('/')[4]
        if '?' in url_split:
            key_word = re.findall('(.*?)\?', url_split)[0]
        else:
            key_word = url_split

        return key_word

    def all_page(self):
        url = self.url.split('/')
        url = '/'.join(url[:4]) + '/' + self.__get_keyword

        for x in range(1, self.max_page + 1):
            re_url = url + '/' + str(x) + '?sort=new'
            yield re_url

    def fun_获取单页(self, url: str):
        html = HTMLDown(url=url, cookie=self.cookie).html

        for ma in html.find('ul.mb-box.masonry-element.clearfix.tpl-ul > li.li-box.search_keyword_statis_js'):
            url = list(ma.find('a', first=True).absolute_links)[0]
            script = ma.find('script', first=True).text
            img = json.loads(script).get('contentUrl')
            yield MaterialType(
                url=url,
                img=img,
                hash=sha256(url.encode('utf-8')).hexdigest()
            )

    def main(self):
        for page in self.all_page():
            print(page)
            for ma_obj in self.fun_获取单页(url=page):
                yield ma_obj


if __name__ == '__main__':
    from pprint import pprint

    scpt = SCPngTree(
        'https://pngtree.com/so/rabbit?sort=new', 20, ''
    )
    for obj in scpt.main():
        pprint(obj)
