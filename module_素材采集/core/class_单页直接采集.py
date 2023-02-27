from hashlib import sha256

from requests_html import HTML

from module_素材采集.core.model import MaterialType


class SCSinglePage:
    def __init__(self, html: str, url: str):
        self.html = HTML(html=html)
        self.url = url

    def taobao(self):
        ma_list = self.html.find(r'#J_ShopSearchResult > div > div.shop-hesper-bd.grid > div > dl')
        for ma in ma_list:
            url = 'https:' + ma.find('.photo a', first=True).attrs.get('href')
            img = 'https:' + ma.find('.photo a img', first=True).attrs.get('src')
            img = img.replace('_180x180.jpg', '')

            yield MaterialType(url=url, img=img, hash=sha256(url.encode('utf-8')).hexdigest())

    def qiantu(self):
        for ma in self.html.find(
                '.pic-container.qtd-card-container > .qtd-card.qtas-pic-card.qtd-card-a.qtd-normal-card'):
            url_find = ma.find('a', first=True)
            url = list(url_find.absolute_links)[0]

            img_find = url_find.find('img.lazy', first=True)
            img = 'https:' + img_find.attrs.get('data-original')

            yield MaterialType(url=url, img=img, hash=sha256(url.encode('utf-8')).hexdigest())

    def baotu(self):
        for ma in self.html.find(
                '.search-list.box-bg-search.box-bottom-gradient.clearfix > .jx-logo-rela.pic-box.pr-container '
        ):
            url = list(ma.find('a.jump-details', first=True).absolute_links)[0]
            hash256 = sha256(url.encode('utf-8')).hexdigest()

            img_element = ma.find('a.jump-details img', first=True)
            if img_element is None:
                continue

            img = img_element.attrs.get('src')
            if img is None:
                img = img_element.attrs.get('data-url')

            img = 'https:' + img

            yield MaterialType(url=url, img=img, hash=hash256)

    def qianku(self):
        for ma in self.html.find(
                '.clearfix.data-list.dataList.V-maronyV1.Vmarony .wall-column .fl.marony-item.ys a.img-box'
        ):
            url = 'https:' + ma.attrs.get('href')
            img = 'https:' + ma.find('img.lazy', first=True).attrs.get('data-original')
            yield MaterialType(url=url, img=img, hash=sha256(url.encode('utf-8')).hexdigest())

    def main(self):
        if '58pic.com' in self.url:
            return self.qiantu()

        elif 'ibaotu.com' in self.url:
            return self.baotu()

        elif '588ku.com' in self.url:
            return self.qianku()

        elif 'taobao.com' in self.url:
            return self.taobao()
