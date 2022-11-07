from functools import cached_property
from pathlib import Path

import zhconv
from PIL import Image, ImageFont, ImageDraw
from faker import Faker
from fontTools.ttLib import TTFont

from module_素材处理.core.setting import IMG_PATH, FONT_PATH
from module_素材处理.core.素材文件夹功能.FontToPIL.fun_随机抽取一句话 import GetShiJu


class FontToPIL:
    """
    传递进来一个字体文件
    生成一个图片
    并保存
    """

    def __init__(self, font_path: Path, tb_name: str):
        self.font_path = font_path
        self.font_obj = TTFont(font_path.as_posix())
        self.tb_name = tb_name

    @cached_property
    def text_map(self):
        return self.font_obj.getBestCmap()

    def is_english(self):
        if len(self.text_map) < 1000:
            return True

        return False

    def is_chinese(self):
        if len(self.text_map) >= 1000:
            return True

        return False

    def has_text(self, text: str):
        for single_text in text:
            if ord(single_text) not in self.text_map:
                return False

        return True

    def fun_生成单词(self):
        if self.is_chinese():
            word_text = GetShiJu().main()

            get_num = 0
            while self.has_text(word_text) is False:
                word_text = GetShiJu().main()

                if get_num > 50:
                    word_text = zhconv.convert(word_text, 'zh-hant')

                    if get_num > 100:
                        word_text = 'Hello FanTong Design'

                        break

                get_num += 1
        else:
            faker = Faker('en_US')
            word_text = faker.sentence(nb_words=2).title()
            word_text = str(word_text).replace('.', '')

        return word_text

    @staticmethod
    def addTransparency(img, factor=0.7):
        img = img.convert('RGBA')
        with Image.new('RGBA', img.size, (0, 0, 0, 0)) as img_blender:
            img = Image.blend(img_blender, img, factor)

        return img

    def fun_制作背景(self):
        im = Image.open(
            (IMG_PATH / self.tb_name / '字体背景.png').as_posix()
        )
        return im

    def fun_图片写字(self):
        im = self.fun_制作背景()
        title_text = self.fun_生成单词()
        info_text = self.fun_字体信息()
        gutter = 50

        # 计算标题尺寸
        title_font_size = 120
        title_true_font = ImageFont.truetype(self.font_path.as_posix(), size=title_font_size)
        title_text_size = title_true_font.getsize(title_text)

        while title_text_size[0] > 1300:
            title_font_size -= 1
            title_true_font = ImageFont.truetype(self.font_path.as_posix(), size=title_font_size)
            title_text_size = title_true_font.getsize(title_text)

        # 计算信息尺寸
        info_font_size = 24
        info_true_font = ImageFont.truetype(
            font=(FONT_PATH.parent / 'MISans' / 'MiSans-Regular.ttf').as_posix(), size=info_font_size
        )
        info_width_height = info_true_font.getsize(info_text)

        # 计算标题字体高度
        ori_height = im.height - gutter - info_width_height[1]
        left = int((im.width - title_text_size[0]) / 2)
        top = int((ori_height - title_text_size[1]) / 2)

        draw = ImageDraw.Draw(im)
        draw.text((left, top), title_text, fill=(60, 60, 90), font=title_true_font)

        # 计算信息文字的坐标
        left = int((im.width - info_width_height[0]) / 2)
        top = im.height - gutter - info_width_height[1]
        draw.text((left, top), info_text, fill=(60, 60, 90), font=info_true_font)

        return im

    @staticmethod
    def text_is_chinese(string):
        for ch in string:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False

    def fun_字体信息(self):
        name_list = []
        font_name = ''

        names = self.font_obj['name'].names
        for nt in names:
            if nt.nameID == 4 or nt.nameID == 1:
                name_list.append(str(nt))

        for string_text in name_list:
            if self.text_is_chinese(string_text):
                font_name = string_text

        if font_name == '':
            name_list.sort(key=lambda k: len(k), reverse=True)
            font_name = name_list[0]

        if self.is_chinese() is True:
            font_name += ' (中文字体)'
        else:
            font_name += ' (英文字体)'

        if self.tb_name == '饭桶设计':
            font_name += ' 饭桶设计 ftdesign.taobao.com'
        elif self.tb_name == '小夕素材':
            font_name += ' 小夕素材 xdscp.taobao.com'

        return font_name

    def main(self):
        png_path = self.font_path.with_suffix('.png')
        if png_path.exists() is True:
            print(f'图片存在不保存')
            return

        im = self.fun_图片写字()

        im.save(png_path.as_posix())
        print(f'图片保存成功:{png_path.as_posix()}')

        im.close()
        self.font_obj.close()


if __name__ == '__main__':

    def del_all_png():
        for num, in_file in enumerate(Path(r'G:\饭桶设计\1000-1999\1015\1015').rglob('*')):

            in_file: Path
            print(in_file.as_posix())

            if in_file.is_file() and in_file.suffix.lower() == '.png':
                in_file.unlink()


    def export_font_png():
        for num, in_file in enumerate(Path(r'G:\饭桶设计\1000-1999\1015\1015').rglob('*')):
            in_file: Path
            print(in_file.as_posix())

            if in_file.is_file() and in_file.suffix.lower() in ['.otf', '.ttf']:
                try:
                    fi = FontToPIL(font_path=in_file, tb_name='饭桶设计')
                    fi.main()
                except:
                    pass
                else:
                    del fi


    del_all_png()
    export_font_png()
