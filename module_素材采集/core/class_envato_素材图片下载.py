import json
import socket
from functools import cached_property
from pathlib import Path

from module_素材采集.core.class_htmldown import HTMLDown


class SCEnvatoPICDown:
    def __init__(self, url: str):
        self.url = url

    @cached_property
    def down_path(self):
        if socket.gethostname() == 'wuweihua':
            return Path(r'G:\DOWN')

        return Path(r'G:\DOWN')

    @cached_property
    def material_dict(self) -> dict:
        """获取包含素材信息的字典"""
        html = HTMLDown(self.url).html
        script_text = ''

        for script_element in html.find('script'):
            if 'window.INITIAL_HYDRATION_DATA' in script_element.text:
                script_text: str = script_element.text

        script_text = script_text.replace('window.INITIAL_HYDRATION_DATA=', '')
        script_text = script_text.replace(';', '')
        script_text = script_text.replace('\\"', "'")
        script_text = script_text.replace('"flat"', '')
        script_text = script_text.replace(',]', ']')
        script_text = script_text.replace(',,', ',')

        script_text: dict = json.loads(script_text)
        material_dict: dict = script_text.get('page').get('data').get('item')

        return material_dict

    @cached_property
    def img_url_list(self):
        """获取图片列表"""
        img_list = [self.material_dict.get('coverImage')]
        img_list.extend(self.material_dict.get('previewImages'))

        img_url_list = []

        img_size = ['w2740', 'w1370', 'w1170', 'w900']
        for img_obj in img_list:
            img_obj: dict
            for in_size in img_size:
                url = img_obj.get(in_size)
                if url is not None:
                    img_url_list.append(url)
                    break

        return img_url_list

    @cached_property
    def material_down_path(self):
        """素材下载目录"""
        ma_down_path = self.down_path / self.material_dict.get('slug')
        if ma_down_path.exists() is False:
            ma_down_path.mkdir()

        return ma_down_path

    def main(self):
        num = 1
        for img in self.img_url_list:
            png_path = self.material_down_path / f'{num}.png'
            print(f'下载图片到：{png_path.as_posix()}')

            if png_path.exists() is True:
                num += 1
                print(f'图片存在，不下载:{png_path.as_posix()}')
                continue

            png_path.write_bytes(HTMLDown(img).content)
            num += 1

    def fun_目录合并(self):
        for in_dir in self.down_path.iterdir():
            if in_dir.is_dir():
                stem = in_dir.stem

                for in_file in self.down_path.iterdir():
                    if in_file.is_file() and stem in in_file.stem:

                        new_path = self.down_path / '新建文件夹'
                        num = 1
                        while new_path.exists() is True:
                            new_path = self.down_path / f'新建文件夹 ({num})'
                            num += 1
                        new_path.mkdir()

                        in_dir_new_name = new_path / in_dir.name
                        in_dir.rename(in_dir_new_name)

                        in_file_new_name = new_path / in_file.name
                        in_file.rename(in_file_new_name)


if __name__ == '__main__':
    SCEnvatoPICDown('https://elements.envato.com/presentation-mockup-DDFL8GD').main()
