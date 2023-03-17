import socket
from functools import cached_property
from urllib.parse import urlparse

from requests_html import HTMLSession, HTML, user_agent


class HTMLDown:
    def __init__(self, url: str, cookie: str = '', use_proxy: bool = True):
        self.url = url

        self.headers = {
            'user-agent': user_agent(),
            'referer': self.fun_获取链接的HOST,
            'cookie': cookie.encode('utf-8')
        }
        self.use_proxy = use_proxy

        self.get_port()

    session = HTMLSession()
    port_list = [7890, 45678]
    port = None
    ip = '192.168.0.101'
    proxies_header = 'http'

    @cached_property
    def fun_获取链接的HOST(self):
        x = urlparse(self.url)
        referer_url = f'{x.scheme}://{x.netloc}'
        return referer_url

    def get_port(self):
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.settimeout(1)

        for in_port in self.port_list:
            try:
                sk.connect((self.ip, in_port))
            except Exception:
                pass
            else:
                self.port = in_port

    @cached_property
    def res(self):
        if self.port is None or self.use_proxy is False:
            print('直接连接')
            self.session.trust_env = False
            return self.session.get(self.url, headers=self.headers)

        else:
            print(f'代理端口：{self.port}')
            proxies = dict(
                http=f'{self.proxies_header}://{self.ip}:{self.port}',
                https=f'{self.proxies_header}://{self.ip}:{self.port}',
            )
            return self.session.get(self.url, proxies=proxies, headers=self.headers)

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
