from hashlib import sha256
from typing import Generator, List

from module_素材采集.core.class_htmldown import HTMLDown
from module_素材采集.core.model import MaterialType
import re


class SCQianKu:
    def __init__(self, start_url: str, max_page: int, cookie: str = ''):
        # if 'default' not in start_url:
        #     start_url = start_url.replace('-1-1/', '-1-0-0-0-0-default-0-1/')

        self.start_url = self.fun_处理起始页(start_url)
        self.max_page = max_page
        self.cookie = cookie

    @staticmethod
    def fun_处理起始页(start_url: str):
        if start_url[-1] != '/':
            return start_url + '/'

        return start_url

    def fun_列表页构建(self):
        for x in range(1, self.max_page + 1):
            url = re.sub('-(\d+)/', f'-{x}/', self.start_url)
            yield url

    def fun_获取单页(self, url: str) -> Generator:
        html = HTMLDown(url, cookie=self.cookie).html
        ma_list = html.find('.fl > .center-box > a.img-box')
        for ma in ma_list:
            url = 'https:' + ma.attrs.get('href')

            ori_src: str = ma.find('img.lazy', first=True).attrs.get('data-original')
            img = 'https:' + ori_src.strip()
            yield MaterialType(url=url, img=img, hash=sha256(url.encode('utf-8')).hexdigest())

    def main(self) -> List[MaterialType]:
        for url in self.fun_列表页构建():
            print(f'开始采集页面：{url}')
            for ma in self.fun_获取单页(url):
                yield ma


if __name__ == '__main__':
    sc_qk = SCQianKu(
        start_url='https://588ku.com/moban/7769450-new-0-0-0-0-0-0-2-1',
        cookie='',
        max_page=10
    )
    for page in sc_qk.fun_列表页构建():
        print(page)
