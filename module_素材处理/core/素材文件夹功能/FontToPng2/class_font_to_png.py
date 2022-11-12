from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Tuple

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from faker import Faker
from fontTools.ttLib.ttFont import TTFont
from peewee import fn
from pypinyin import lazy_pinyin
import zhconv

from module_素材处理.core.setting import IMG_PATH
from module_素材处理.core.图片编辑 import PICEdit
from module_素材处理.core.素材文件夹功能.FontToPng2.model import TangShi
from module_素材处理.core.素材文件夹功能.FontToPng2.model import database


@dataclass
class FontSize:
    width: int
    height: int
    top_height: int


class FontToPng:
    def __init__(self, font_path: Path, tb_name: str):
        self.font_path = font_path
        self.tb_name = tb_name

    font_size = 180
    font_color = (60, 60, 90)
    bg_color = (255, 255, 255)

    watermark_color = (120, 120, 120)
    watermark_gutter = 80

    bg_margin = 150

    font_width = 1500
    font_height = 300

    has_watermark = True

    @property
    def png_path(self):
        return self.font_path.with_suffix('.png')

    @cached_property
    def font_obj(self):
        return TTFont(self.font_path.as_posix())

    @cached_property
    def font_cmap(self):
        fc = self.font_obj.getBestCmap()
        return fc

    @cached_property
    def is_chinese_font(self):
        if len(self.font_cmap) > 1000:
            return True

        return False

    @staticmethod
    def has_chinese(string):
        for ch in string:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True

        return False

    @staticmethod
    def fun_处理NAME(text_str: str):
        re_str = (
            (' ', '_'),
        )

        for re_s in re_str:
            text_str = text_str.replace(re_s[0], re_s[1])

        return text_str

    @cached_property
    def font_name(self):
        font_name = ''
        name_list = []
        names = self.font_obj['name'].names
        for nt in names:
            if nt.nameID == 4 or nt.nameID == 1:
                name_list.append(str(nt))

        for nt_str in name_list:
            if self.has_chinese(nt_str):
                font_name = nt_str

        if font_name == '':
            font_name = max(name_list)

        font_name = self.fun_处理NAME(font_name)

        return font_name

    def fun_制作背景(self, size: Tuple[int, int]) -> Image.Image:
        bg = Image.new('RGBA', size, self.bg_color)
        if self.has_watermark is True:
            # 处理水印
            watermark = Image.open((IMG_PATH / self.tb_name / 'site_logo.png').as_posix())
            watermark = PICEdit.fun_颜色覆盖(img=watermark, color=self.watermark_color)
            watermark = watermark.rotate(15, expand=True, resample=0)
            watermark.thumbnail((150, 150), resample=1)
            watermark = PICEdit.fun_图片添加不透明度(watermark, .05)

            # 粘贴水印
            left, top = 0, 0 - int(watermark.height / 2)

            num = 0
            while top < bg.height:
                bg.paste(watermark, (left, top), watermark)
                left += watermark.width + self.watermark_gutter
                if left >= bg.width:
                    if num % 2 == 0:
                        left = 0 - int(watermark.width / 2)
                    else:
                        left = 0

                    top += watermark.height + self.watermark_gutter
                    num += 1

            watermark.close()

        return bg

    def fun_判断字体是否包含本文(self, text: str) -> bool:
        for ch in text:
            if ord(ch) not in self.font_cmap:
                return False

        return True

    @staticmethod
    def fun_随机获取成语() -> str:
        with database:
            chengyu = TangShi.select().order_by(fn.Random())[0].ci

        chengyu = chengyu.replace('，', ' ')
        chengyu = chengyu.replace('。', '')
        chengyu = zhconv.convert(chengyu, 'zh-hans')
        return chengyu

    @staticmethod
    def fun_随机获取英文单词() -> str:
        faker = Faker('en_US')
        word_text = faker.sentence(nb_words=2).title()
        word_text = str(word_text).replace('.', '')
        return word_text

    def fun_确定成语(self):
        if self.is_chinese_font:
            word = self.fun_随机获取成语()

            num = 0
            while self.fun_判断字体是否包含本文(word) is False:
                if num < 100:
                    word = self.fun_随机获取成语()
                elif 200 > num >= 100:
                    word = zhconv.convert(self.fun_随机获取成语(), 'zh-hant')
                else:
                    word = 'hello word'
                    break

                num += 1
        else:
            word = self.fun_随机获取英文单词()

        return word

    def fun_获取字体大小(self, word: str, font_size: int) -> FontSize:
        true_font = ImageFont.truetype(self.font_path.as_posix(), size=font_size)
        bbox = true_font.getbbox(word)
        return FontSize(
            width=bbox[2],
            height=bbox[3],
            top_height=bbox[1]
        )

    @staticmethod
    def fun_汉字转拼音(word: str):
        pinyin_str = lazy_pinyin(word)
        pinyin_str = ' '.join(pinyin_str)
        pinyin_str = pinyin_str.title()
        return pinyin_str

    def fun_make_pil(self, word: str):
        font_bg = self.fun_制作背景(size=(self.font_width, self.font_height))
        draw = ImageDraw.Draw(font_bg)

        # 确定标题的字体
        font_bbox = self.fun_获取字体大小(word, self.font_size)

        while font_bbox.width > self.font_width - self.bg_margin:
            self.font_size -= 1
            font_bbox = self.fun_获取字体大小(word, self.font_size)

        while font_bbox.height > self.font_height - self.bg_margin:
            self.font_size -= 1
            font_bbox = self.fun_获取字体大小(word, self.font_size)

        # 写标题
        left = int((font_bg.width - font_bbox.width) / 2)
        top = int((font_bg.height - font_bbox.height) / 2) - int(font_bbox.top_height / 2)
        draw.text(
            (left, top), word, fill=self.font_color, font=ImageFont.truetype(self.font_path.as_posix(), self.font_size)
        )

        return font_bg

    def main(self):
        if self.png_path.exists() is False:
            bg = self.fun_make_pil(self.fun_确定成语())
            bg.save(self.png_path.as_posix())


if __name__ == '__main__':
    ftp = FontToPng(
        font_path=Path(r'G:\饭桶设计\1000-1999\1015\1015\000_099\饭桶设计(1).otf'),
        tb_name='小夕素材'
    )
    fbg = ftp.fun_make_pil(ftp.fun_确定成语())
    fbg.show()
    # up_path = Path(r'C:\Users\wuweihua\Desktop\UPLOAD\1.png')
    # fbg.save(up_path.as_posix())
