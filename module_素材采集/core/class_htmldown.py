from functools import cached_property
from urllib.parse import urlparse

from requests_html import HTML
from requests_html import HTMLSession
from requests_html import user_agent


class HTMLDown:
    def __init__(self, url: str, cookie: str = '', use_proxy: bool = True):
        self.url = url

        self.headers = {
            'user-agent': user_agent(),
            'referer':    self.fun_获取链接的HOST,
            'cookie':     cookie.encode('utf-8')
        }
        self.use_proxy = use_proxy

    session = HTMLSession()
    port = 7890
    ip = '192.168.0.101'
    proxies_header = 'http'

    @cached_property
    def fun_获取链接的HOST(self):
        x = urlparse(self.url)
        referer_url = f'{x.scheme}://{x.netloc}'
        return referer_url

    @cached_property
    def res(self):
        requre_proxy = ''
        proxies = dict(
            http=f'{self.proxies_header}://{self.ip}:{self.port}',
            https=f'{self.proxies_header}://{self.ip}:{self.port}',
        )
        try:
            res = self.session.get(self.url, proxies=proxies, headers=self.headers)
            requre_proxy = '代理连接'
        except:
            self.session.trust_env = False
            res = self.session.get(self.url, headers=self.headers)
            requre_proxy = '直接连接'

        print(requre_proxy)
        return res

    @cached_property
    def html(self) -> HTML:
        html = self.res.html
        self.res.close()
        self.session.close()

        return html

    @cached_property
    def content(self):
        content = self.res.content
        self.res.close()
        self.session.close()

        return content


if __name__ == '__main__':
    hd = HTMLDown('https://qq.com')
    print(
        hd.html.find('title', first=True).text
    )
