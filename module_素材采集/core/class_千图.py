import json
import re
from hashlib import sha256

from module_素材采集.core.class_htmldown import HTMLDown
from module_素材采集.core.model import MaterialType


class SCQianTu:
    def __init__(self, start_url: str, max_page: int, cookie: str = ''):
        self.start_url = self.fun_构建起始页(start_url)
        self.max_page = max_page
        self.cookie = cookie

    @staticmethod
    def fun_构建起始页(start_url: str):
        end_str = '?is_ajax=1&is_new=1'
        if end_str not in start_url:
            return start_url + end_str

    def fun_构建列表页(self):
        # https://www.58pic.com/tupian/244776038-0-0-id-1-0-0-0_2_0_0_0_0_0-0-0-0-0-0-0-0-0.html
        # https://www.58pic.com/tupian/244776038-0-0-id-1-0-0-0_2_0_0_0_0_0-0-0-0-0-0-0-0-2.html?is_ajax=1&is_new=1
        for x in range(1, self.max_page + 1):
            url = re.sub(r'-?(\d*?)\.html', f'-{x}.html', self.start_url)
            yield url

    def fun_获取单页(self, url: str):
        res = HTMLDown(url, cookie=self.cookie).html
        data_dict: dict = json.loads(res.html)
        data = data_dict.get('data').get('pics')
        for obj in data:
            obj: dict
            url = f'https://www.58pic.com/newpic/{obj.get("id")}.html'
            img = f"https:{obj.get('picurl')}"
            print(url, img, '\n')
            yield MaterialType(url=url, img=img, hash=sha256(url.encode('utf-8')).hexdigest())

    def main(self):
        for url in self.fun_构建列表页():
            for ma in self.fun_获取单页(url):
                yield ma


if __name__ == '__main__':
    for ma_obj in SCQianTu(
            start_url=r'https://www.58pic.com/tupian/tunianhaibao-0-0-default-1-0-%E5%85%94%E5%B9%B4%E6%B5%B7%E6%8A%A5-0_2_0_0_0_0_0-0-0-0-0-0-0-0-2.html',
            max_page=10).main():
        print(ma_obj)
