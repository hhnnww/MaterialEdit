from functools import cached_property
from pathlib import Path
from typing import Literal, Tuple

from PIL import Image, ImageFont, ImageDraw

from module_素材处理.core.setting import FONT_PATH
from module_素材处理.core.图片编辑.fun_边框删除 import DelPILBorder

FONT_WEIGHT_TYPE = Literal['l', 'r', 'm', 'b', 'h']


class TextToPIL:
    def __init__(self, text: str, font_weight: FONT_WEIGHT_TYPE, font_size: int, text_color: Tuple, bg_color: Tuple):
        self.text = text
        self.font_weight = font_weight
        self.font_size = font_size
        self.text_color = text_color
        self.bg_color = bg_color

    @cached_property
    def fun_根据字重选择字体(self) -> Path:
        font_name = ''

        match self.font_weight:
            case 'l':
                font_name = 'MiSans-Light.ttf'
            case 'm':
                font_name = 'MiSans-Medium.ttf'
            case 'r':
                font_name = 'MiSans-Regular.ttf'
            case 'b':
                font_name = 'MiSans-Bold.ttf'
            case 'h':
                font_name = 'MiSans-Heavy.ttf'

        font_path = FONT_PATH / 'MISans' / font_name
        if font_path.exists() is False:
            raise IndexError('字体路径不存在')

        return font_path

    @cached_property
    def fun_构建TRUE字体(self):
        true_font = ImageFont.truetype(
            font=self.fun_根据字重选择字体.as_posix(),
            size=self.font_size
        )
        return true_font

    @cached_property
    def fun_获取图片尺寸(self):
        true_font = self.fun_构建TRUE字体
        bg_size = true_font.getbbox(text=self.text)
        return bg_size[2], bg_size[3]

    def main(self) -> Image.Image:
        bg = Image.new('RGBA', self.fun_获取图片尺寸, self.bg_color)
        draw = ImageDraw.Draw(bg)
        draw.text((0, 0), text=self.text, fill=self.text_color, font=self.fun_构建TRUE字体)
        bg = DelPILBorder(bg, None).main()
        return bg


if __name__ == '__main__':
    tp = TextToPIL(
        '海报', 'l', 290, (0, 0, 0), (255, 255, 255)
    ).main()

    tp.show()
