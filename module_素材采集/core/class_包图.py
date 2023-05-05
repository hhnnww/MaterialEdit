import re
from hashlib import sha256
from typing import Generator, List

from module_素材采集.core.class_htmldown import HTMLDown
from module_素材采集.core.model import MaterialType


class SCBaoTu:
    def __init__(self, start_url: str, max_page: int, cookie: str = ''):
        if '?' in start_url:
            start_url = re.sub(r'\?(.*)?', '', start_url)

        if 'tupians' not in start_url:
            start_url = start_url.replace('tupian', 'tupians')

        self.start_url = start_url
        self.max_page = max_page
        self.cookie = cookie

    def fun_列表页构建(self):
        for x in range(1, self.max_page + 1):
            url = re.sub(r'-?(\d+?)\.html', f'-{x}.html', self.start_url)
            yield url

    def fun_获取单页(self, url: str) -> Generator:
        html = HTMLDown(url, cookie=self.cookie).html

        ma_list = html.find('body > div.page-body.skin-wrap.body-background-gradient > div.bt-body.search.clearfix > div.search-list.box-bg-search.box-bottom-gradient.clearfix > dl')

        for ma in ma_list:
            if 'searchAdver' in ma.attrs.get('class'):
                print('广告')
                continue

            url = list(ma.find('a', first=True).absolute_links)[0]
            print('素材URL:' + url)
            hash256 = sha256(url.encode('utf-8')).hexdigest()

            # 开始查找图片
            img_element = ma.find('a img', first=True)
            if img_element is None:
                continue

            img = img_element.attrs.get('data-url')
            if img is None:
                img = img_element.attrs.get('src')

            img = 'https:' + img
            print('素材图片:' + img + '\n')

            yield MaterialType(url=url, img=img, hash=hash256)

    def main(self) -> List[MaterialType]:
        if self.max_page > 1:
            for url in self.fun_列表页构建():
                print(url)
                for ma in self.fun_获取单页(url):
                    yield ma

        else:
            print(f'单独采集')
            for ma in self.fun_获取单页(self.start_url):
                yield ma


if __name__ == '__main__':
    cookie = """__is_small_screen=0; wx_oal_type=0; Hm_lvt_2b0a2664b82723809b19b4de393dde93=1668761293; FIRSTVISITED=1681790466.457; last_auth=2; ISREQUEST=1; WEBPARAMS=is_pay=1; md_session_id=20230505001034788; user_refers=a%3A2%3A%7Bi%3A0%3Bs%3A6%3A%22ibaotu%22%3Bi%3A1%3Bs%3A6%3A%22ibaotu%22%3B%7D; new_edition_type_v4=1; _sh_hy=a%3A1%3A%7Bi%3A0%3Ba%3A2%3A%7Bs%3A4%3A%22name%22%3Bs%3A6%3A%22%E6%B5%B7%E6%8A%A5%22%3Bs%3A5%3A%22count%22%3Bi%3A8888%3B%7D%7D; Hm_lvt_4df399c02bb6b34a5681f739d57787ee=1681790466,1683268636; md_session_expire=1800; bt_guid=24f59754900da3d2b90d76c8dc418243; Hm_lpvt_4df399c02bb6b34a5681f739d57787ee=1683269212; referer=http%3A%2F%2Fibaotu.com%2F%3Fm%3DsearchAnaly%26a%3DsidGather%26sp%3D1%26sid%3D40%26callback%3DjQuery112409327387677503582_1683269225578%26_%3D1683269225579"""
    for ma_obj in SCBaoTu(
            start_url='https://ibaotu.com/tupians/haibao/6-0-0-0-0-1-c0_1-2.html', max_page=3, cookie=cookie
    ).main():
        print(ma_obj)
