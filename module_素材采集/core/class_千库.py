from hashlib import sha256
from typing import Generator, List

from module_素材采集.core.class_htmldown import HTMLDown
from module_素材采集.core.model import MaterialType
import re


class SCQianKu:
    def __init__(self, start_url: str, max_page: int, cookie: str = ''):
        # if 'default' not in start_url:
        #     start_url = start_url.replace('-1-1/', '-1-0-0-0-0-default-0-1/')

        self.start_url = start_url
        self.max_page = max_page
        self.cookie = cookie

    def fun_列表页构建(self):
        for x in range(1, self.max_page + 1):
            # https://588ku.com/so/funvjiehaibao-0-0-0-0-0-default-0-2/
            # url = self.start_url.replace('-1/', f'-{x}/')
            url = re.sub('-0-(\d+)/', f'-0-{x}/', self.start_url)
            yield url

    def fun_获取单页(self, url: str) -> Generator:
        html = HTMLDown(url, cookie=self.cookie).html
        ma_list = html.find('.fl.model > .center-box > a.img-box')

        for ma in ma_list:
            url = 'https:' + ma.attrs.get('href')
            img = 'https:' + ma.find('img.lazy', first=True).attrs.get('data-original')
            yield MaterialType(url=url, img=img, hash=sha256(url.encode('utf-8')).hexdigest())

    def main(self) -> List[MaterialType]:
        for url in self.fun_列表页构建():
            print(f'开始采集页面：{url}')
            for ma in self.fun_获取单页(url):
                yield ma


if __name__ == '__main__':
    for ma_obj in SCQianKu(
            start_url='https://588ku.com/so/102376015-1-0-0-0-0-default-0-2/',
            cookie='',
            max_page=10
    ).main():
        print(ma_obj)
