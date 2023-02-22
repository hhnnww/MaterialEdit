import re
from hashlib import sha256

from module_素材采集.core.class_htmldown import HTMLDown
from module_素材采集.core.model import MaterialType


class SCCaoTuLianMeng:
    def __init__(self, start_url: str, max_page: int, cookie: str = ''):
        self.start_url = start_url
        self.max_page = max_page
        self.cookie = cookie

    def fun_make_page_list(self):
        if 'page' not in self.start_url:
            self.start_url = self.start_url + '/page/1'

        for x in range(1, self.max_page + 1):
            url = re.sub('page/(\d+)', f'page/{x}', self.start_url)
            yield url

    def fun_get_material_from_page(self, page_url: str):
        html = HTMLDown(url=page_url, cookie=self.cookie).html
        material_list = html.find(r'#posts > div.post')

        for material in material_list:
            url_element = material.find('.img a', first=True).attrs.get('href')
            img_element = material.find('.img img', first=True).attrs.get('src')

            yield MaterialType(url=url_element, img=img_element, hash=sha256(url_element.encode('utf-8')).hexdigest())

    def main(self):
        for page_url in self.fun_make_page_list():
            for ma_obj in self.fun_get_material_from_page(page_url):
                yield ma_obj


if __name__ == '__main__':
    sc_ctlm = SCCaoTuLianMeng(
        start_url=r'https://www.cnwhc.com/zhengticj',
        max_page=44,
    )

    for ma in sc_ctlm.fun_get_material_from_page(page_url=r'https://www.cnwhc.com/zhengticj'):
        print(ma)
