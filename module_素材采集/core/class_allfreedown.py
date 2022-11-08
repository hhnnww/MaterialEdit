from hashlib import sha256

from module_素材采集.core.class_htmldown import HTMLDown
from module_素材采集.core.model import MaterialType


class SCAllFreeDown:
    def __init__(self, start_url: str, max_page: int, cookie: str = ''):
        self.start_url = start_url
        self.max_page = max_page
        self.cookie = cookie

    @staticmethod
    def all_page():
        # https://all-free-download.com/?a=G&t=avs&q=&rk=any&k=free-vector&lc=all&or=new&p=6
        for x in range(1, 100):
            yield f'https://all-free-download.com/?a=G&t=avs&q=&rk=any&k=free-vector&lc=all&or=new&p={x}'

    def get_material(self, url: str):
        html = HTMLDown(url, cookie=self.cookie).html

        ma_list = html.find(
            'body div.container-fluid.pb-3 div.row.row-cols-1.row-cols-sm-1.row-cols-md-5.row-cols-xl-5.row-cols-xxl-5 .col .grid-item.grid-item-cell')
        for ma in ma_list:
            url = list(ma.find('.item-image-cover a', first=True).absolute_links)[0]
            img = ma.find('.item-image-cover a img', first=True).attrs.get('src')
            yield MaterialType(url=url, img=img, hash=sha256(url.encode('utf-8')).hexdigest())

    def main(self):
        for url in self.all_page():
            for ma in self.get_material(url):
                yield ma
