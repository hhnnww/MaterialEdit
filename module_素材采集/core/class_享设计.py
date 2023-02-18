import json
import re
from functools import cached_property
from hashlib import sha256

from module_素材采集.core.class_htmldown import HTMLDown
from module_素材采集.core.model import MaterialType


class SCXiangSheJi:
    def __init__(self, start_url: str, max_page: int, cookie: str = ''):
        self.start_url = start_url
        self.max_page = max_page
        self.cookie = cookie

    @cached_property
    def get_keyword(self) -> str:
        search_key = re.findall(r'/search-(.+?)-all', self.start_url)[0]
        return search_key

    def fun_构建列表页(self):
        search_key = self.get_keyword
        for x in range(1, self.max_page + 1):
            yield f'https://www.design006.com/Home/Index/get_data_index2/p/{x}/keywords/{search_key}/color_id/all/work_type_id/all/option_most/2/is_free/all/typesetting/all/sort/0/format/all'

    def fun_获取单页(self, url: str):
        html = HTMLDown(url=url, cookie=self.cookie).html

        ma_list = json.loads(html.html)
        ma_list = ma_list.get('result')

        for ma in ma_list:
            # https://imgs.design006.com/202302/Design006_TEbaWAYyDF.jpg?x-oss-process=style/prev_w_460_mh_1600
            img = f'https://imgs.design006.com/{ma.get("preview_image")}?x-oss-process=style/prev_w_460_mh_1600'
            url = f'https://www.design006.com/detail-{ma.get("prefix_id")}{ma.get("id")}'
            print(url)

            yield MaterialType(url=url, img=img, hash=sha256(url.encode('utf-8')).hexdigest())

    def main(self):
        for page_url in self.fun_构建列表页():
            for ma_obj in self.fun_获取单页(page_url):
                yield ma_obj


if __name__ == '__main__':
    sc_xsj = SCXiangSheJi(
        start_url=r'https://www.design006.com/search-%E6%97%85%E6%B8%B8-all-all-2-all-all-all-0-all',
        max_page=10,
        cookie=''
    )
    for ma_o in sc_xsj.main():
        print(ma_o)
