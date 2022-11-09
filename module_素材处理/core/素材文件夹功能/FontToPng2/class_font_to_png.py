from functools import cached_property
from pathlib import Path
from typing import Tuple

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from faker import Faker
from fontTools.ttLib.ttFont import TTFont
from peewee import fn

from module_素材处理.core.setting import IMG_PATH
from module_素材处理.core.图片编辑.fun_单行文字转PIL import TextToPIL
from module_素材处理.core.素材文件夹功能.FontToPng2.model import ChengYu
from module_素材处理.core.素材文件夹功能.FontToPng2.model import database


class FontToPng:
    def __init__(self, font_path: Path, tb_name: str):
        self.font_path = font_path
        self.tb_name = tb_name

    font_size = 280
    font_color = (255, 255, 255)
    bg_color = (0, 40, 165)
    watermark_gutter = 50
    img_border = 200

    @property
    def png_path(self):
        return self.font_path.with_suffix('.png')

    @cached_property
    def font_obj(self):
        return TTFont(self.font_path.as_posix())

    @cached_property
    def font_cmap(self):
        return self.font_obj.getBestCmap()

    @property
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

    @staticmethod
    def fun_图片添加不透明度(img: Image.Image, factor: float = 0.7) -> Image.Image:
        for x in range(img.width):
            for y in range(img.height):
                color = list(img.getpixel((x, y)))
                color[-1] = int(color[-1] * factor)
                img.putpixel((x, y), tuple(color))

        return img

    def fun_制作背景(self, size: Tuple[int, int]) -> Image.Image:
        # 处理水印
        watermark = Image.open((IMG_PATH / self.tb_name / 'site_logo.png').as_posix())
        watermark = watermark.rotate(15, expand=True, resample=0)
        watermark.thumbnail((150, 150), resample=1)
        watermark = self.fun_图片添加不透明度(watermark, .05)

        # 粘贴水印
        bg = Image.new('RGBA', size, self.bg_color)
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

        return bg

    def fun_判断字体是否包含本文(self, text: str) -> bool:
        for ch in text:
            if ord(ch) not in self.font_cmap:
                return False

        return True

    @staticmethod
    def fun_随机获取成语() -> str:
        with database:
            chengyu = ChengYu.select().order_by(fn.Random())[0]

        return chengyu.ci

    @staticmethod
    def fun_随机获取英文单词() -> str:
        faker = Faker('en_US')
        word_text = faker.sentence(nb_words=2).title()
        word_text = str(word_text).replace('.', '')
        return word_text

    def fun_制作图片信息(self, width: int):
        bg_color = list(self.bg_color)
        bg_color = tuple(bg_color)

        text_pil = TextToPIL(text=self.font_name.upper(), font_weight='l', font_size=34, text_color=self.font_color,
                             bg_color=bg_color).main()

        if self.tb_name == '小夕素材':
            text_2_pil = TextToPIL(text='小夕素材 xdscp.taobao.com'.upper(), font_weight='l', font_size=22,
                                   text_color=self.font_color, bg_color=
                                   bg_color).main()
        else:
            text_2_pil = TextToPIL(text='饭桶设计 ftdesign.taobao.com'.upper(), font_weight='l', font_size=22,
                                   text_color=self.font_color, bg_color=
                                   bg_color).main()

        text_pil.thumbnail((width, width))
        text_2_pil.thumbnail((width, width))
        gutter = 40
        inside_gutter = 15
        height = text_pil.height + (gutter * 2) + text_2_pil.height + inside_gutter

        bg = Image.new('RGBA', (width, height), tuple(bg_color))

        left = int((bg.width - text_pil.width) / 2)
        top = gutter
        bg.paste(text_pil, (left, top), text_pil)

        left = int((bg.width - text_2_pil.width) / 2)
        top += text_pil.height + inside_gutter
        bg.paste(text_2_pil, (left, top), text_2_pil)

        return bg

    def main(self):
        if self.png_path.exists() is False:

            if self.is_chinese_font:
                word = self.fun_随机获取成语()

                num = 0
                while self.fun_判断字体是否包含本文(word) is False:
                    if num < 100:
                        word = self.fun_随机获取成语()
                    else:
                        word = 'hello word'
                        break

                    num += 1
            else:
                word = self.fun_随机获取英文单词()

            true_font = ImageFont.truetype(self.font_path.as_posix(), size=self.font_size)
            bbox = true_font.getbbox(word)
            tf_width = bbox[2]
            tf_height = bbox[3] - bbox[1]

            while tf_width > 1300:
                self.font_size -= 1
                true_font = ImageFont.truetype(self.font_path.as_posix(), size=self.font_size)
                bbox = true_font.getbbox(word)
                tf_width = bbox[2]
                tf_height = bbox[3] - bbox[1]

            while tf_height > 200:
                self.font_size -= 1
                true_font = ImageFont.truetype(self.font_path.as_posix(), size=self.font_size)
                bbox = true_font.getbbox(word)
                tf_width = bbox[2]
                tf_height = bbox[3] - bbox[1]

            bg = self.fun_制作背景(size=(1500, 500))
            draw = ImageDraw.Draw(bg)
            left = int((bg.width - tf_width) / 2)
            top = int((bg.height - tf_height) / 2)

            draw.text(
                (left, top-bbox[1]), word, fill=self.font_color, font=true_font
            )
            # return bg
            bg.save(self.png_path.as_posix())

            # info_pil = self.fun_制作图片信息(width=bg.width)
            # new_bg = Image.new('RGBA', (bg.width, info_pil.height + bg.height), self.bg_color)
            # new_bg.paste(bg, (0, 0), bg)
            # new_bg.paste(info_pil, (0, bg.height), info_pil)
            #
            # new_bg.save(self.png_path.as_posix())


if __name__ == '__main__':
    ftp = FontToPng(
        font_path=Path(r'E:\小夕素材\9000-9999\9261\9261\000_099\小夕素材(1).otf'),
        tb_name='饭桶设计'
    )
    ftp.main()
