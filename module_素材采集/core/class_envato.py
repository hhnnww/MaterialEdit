import re
from module_素材采集.core.class_htmldown import HTMLDown
from module_素材采集.core.model import MaterialType
import json
from hashlib import sha256
from tqdm import tqdm


class SCEnvato:
    def __init__(self, start_url: str, max_page: int, cookie: str = ''):
        if 'pg-' not in start_url.split('/')[-1]:
            start_url = start_url + '/pg-1'

        self.start_url = start_url
        self.max_page = max_page
        self.cookie = cookie

    def fun_列表页(self):
        # https://elements.envato.com/user/helloDigi/graphic-templates?page=1
        if '?page=' not in self.start_url:
            self.start_url = self.start_url + '?page=1'

        for x in range(1, self.max_page + 1):
            url = re.sub('\?page=(\d+)', f'?page={x}', self.start_url)
            yield url

    def fun_列表页中获取素材(self, url):
        html = HTMLDown(url, cookie=self.cookie).html

        script_text = ''

        for in_script in html.find('script'):
            if 'window.INITIAL_HYDRATION_DATA' in in_script.text:
                script_text = in_script.text

        script_text = re.findall('(\{[\s\S]*?});', script_text)[0]

        items: dict = json.loads(script_text)
        items = items.get('page').get('data').get('items')

        for item in items:
            item: dict
            url = f'https://elements.envato.com/item-{item.get("id")}'
            img = ''

            for img_size in ['w632', 'w710', 'w866', 'w900']:
                in_img = item.get('coverImage').get(img_size)
                if in_img is not None:
                    img = in_img

            yield MaterialType(
                url=url,
                img=img,
                hash=sha256(url.encode('utf-8')).hexdigest()
            )

    def main(self):
        for page in tqdm(list(self.fun_列表页()), desc='采集', ncols=100):
            for ma in self.fun_列表页中获取素材(page):
                yield ma


if __name__ == '__main__':
    sce = SCEnvato(
        start_url=r'https://elements.envato.com/graphic-templates/product-mockups/sort-by-latest/pg-2',
        max_page=20
    ).main()
    for ma_obj in sce:
        print(ma_obj)
