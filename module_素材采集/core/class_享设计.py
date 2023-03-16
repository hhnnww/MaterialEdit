import json
import re
from hashlib import sha256

from module_素材采集.core.class_htmldown import HTMLDown
from module_素材采集.core.model import MaterialType


class SCXiangSheJi:
    def __init__(self, start_url: str, max_page: int, cookie: str = ''):
        self.start_url = start_url
        self.max_page = max_page
        self.cookie = cookie

    def fun_构建列表页(self):
        # https://www.design006.com/search-%E6%98%A5-all-all-1-all-all-1-0-2
        # https://www.design006.com/Home/Index/get_data_index2/p/2/keywords/%E6%98%A5/color_id/all/work_type_id/all/option_most/1/is_free/all/typesetting/1/sort/0/format/2

        option_list: str = re.findall(r'/search-([\s\S]*?)$', self.start_url)[0]
        option_list = option_list.split('-')
        key_word = option_list[0]
        material_format = option_list[-1]
        material_sort = option_list[3]
        material_types = option_list[6]

        for x in range(1, self.max_page + 1):
            yield f'https://www.design006.com/Home/Index/get_data_index2/p/{x}/keywords/{key_word}/color_id/all/work_type_id/all/option_most/{material_sort}/is_free/all/typesetting/{material_types}/sort/0/format/{material_format}'

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
