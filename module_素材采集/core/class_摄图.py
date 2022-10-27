import re
from hashlib import sha256
from typing import Generator, List

from module_素材采集.core.class_htmldown import HTMLDown
from module_素材采集.core.model import MaterialType


class SCSheTu:
    def __init__(self, start_url: str, max_page: int, cookie: str = ''):
        self.start_url = start_url
        self.max_page = max_page
        self.cookie = cookie

    def fun_列表页构建(self):
        for x in range(1, self.max_page + 1):
            url = re.sub('-psd-all-\d+?-0', f'-psd-all-{x}-0', self.start_url)
            yield url

    def fun_获取单页(self, url: str) -> Generator:
        html = HTMLDown(url, cookie=self.cookie).html
        ma_list = html.find('#wrapper > div.imgshow.clearfix > div > div.list')

        for ma in ma_list:
            url_find = ma.find('a', first=True)
            url = list(url_find.absolute_links)[0]

            img_find = url_find.find('img.lazy', first=True)
            img = 'https:' + img_find.attrs.get('data-original')

            yield MaterialType(url=url, img=img, hash=sha256(url.encode('utf-8')).hexdigest())

    def main(self) -> List[MaterialType]:
        for url in self.fun_列表页构建():
            for ma in self.fun_获取单页(url):
                yield ma


if __name__ == '__main__':
    for ma_obj in SCSheTu(
            start_url='https://699pic.com/muban-15562298-0-complex-all-0-psd-all-2-0-0-0-0-0-0-all-all-0-0.html', max_page=10
    ).main():
        print(ma_obj)
