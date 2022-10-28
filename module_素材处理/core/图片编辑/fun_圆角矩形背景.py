from typing import Tuple

from PIL import Image, ImageDraw

from module_素材处理.core.setting import IMG_PATH
from module_素材处理.core.图片编辑.fun_颜色覆盖 import fun_颜色覆盖


def fun_圆角矩形背景(width: int, height: int, bg_color: Tuple[int]) -> Image.Image:
    multiple = 5

    # 处理圆形背景
    circle_pil = Image.open(IMG_PATH / '圆角背景.png')
    circle_pil = fun_颜色覆盖(circle_pil, bg_color)
    circle_pil.thumbnail((height * multiple, height * multiple), 1)

    # 画一个正方形
    bg = Image.new('RGBA', (width * multiple, height * multiple), (255, 255, 255, 0))
    draw = ImageDraw.Draw(bg, mode='RGBA')
    draw.rectangle(
        (
            int((height * multiple) / 2),
            0,
            (width * multiple) - int((height * multiple) / 2),
            height * multiple
        ), fill=bg_color, outline=None, width=0
    )

    # 粘贴圆形背景到两边
    bg.paste(circle_pil, (0, 0), circle_pil)
    bg.paste(circle_pil, (bg.width - circle_pil.width, 0), circle_pil)
    bg.thumbnail((width, height), 1)
    circle_pil.close()

    return bg


if __name__ == '__main__':
    fun_圆角矩形背景(width=200, height=200, bg_color=(18, 210, 172))
