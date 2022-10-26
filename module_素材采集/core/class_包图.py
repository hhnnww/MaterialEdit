import re
from hashlib import sha256
from typing import Generator, List

from module_素材采集.core.class_htmldown import HTMLDown
from module_素材采集.core.model import MaterialType


class SCBaoTu:
    def __init__(self, start_url: str, max_page: int, cookie: str = ''):
        self.start_url = start_url
        self.max_page = max_page
        self.cookie = cookie

    def fun_列表页构建(self):
        for x in range(1, self.max_page + 1):
            url = re.sub(r'-?(\d+?)\.html', f'-{x}.html', self.start_url)
            yield url

    def fun_获取单页(self, url: str) -> Generator:
        html = HTMLDown(url, cookie=self.cookie).html
        ma_list = html.find(
            r'body > div.page-body.skin-wrap.body-background-gradient > div.bt-body.search.clearfix > div.search-list.box-bg-search.box-bottom-gradient.clearfix > dl')

        for ma in ma_list:
            url = list(ma.find('a.jump-details', first=True).absolute_links)[0]

            img_element = ma.find('a.jump-details img', first=True)
            if img_element is None:
                continue

            img = img_element.attrs.get('src')
            if img is None:
                img = img_element.attrs.get('data-url')

            img = 'https:' + img

            yield MaterialType(url=url, img=img, hash=sha256(url.encode('utf-8')).hexdigest())

    def main(self) -> List[MaterialType]:
        _ = []
        for url in self.fun_列表页构建():
            for ma in self.fun_获取单页(url):
                _.append(ma)

        return _


if __name__ == '__main__':
    for ma_obj in SCBaoTu(
            start_url='https://ibaotu.com/tupians/wanshengjiehaibao/6-0-0-0-0-1-c0_1-7.html', max_page=10
    ).main():
        print(ma_obj)
