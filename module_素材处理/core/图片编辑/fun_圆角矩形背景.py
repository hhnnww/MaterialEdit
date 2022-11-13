from typing import Tuple

from PIL import Image
from PIL import ImageDraw

from module_素材处理.core.setting import IMG_PATH
from module_素材处理.core.图片编辑.fun_颜色覆盖 import fun_颜色覆盖


def fun_圆角矩形背景(width: int, height: int, bg_color: Tuple[int]) -> Image.Image:
    multiple = 1

    # 处理圆形背景
    circle_pil = Image.open(IMG_PATH / '圆角背景.png')
    circle_pil = fun_颜色覆盖(circle_pil, bg_color)
    circle_pil = circle_pil.resize((height * multiple, height * multiple), 1)

    bg = Image.new('RGBA', (width * multiple, height * multiple), (255, 255, 255, 0))

    # 粘贴圆形背景到两边
    bg.paste(circle_pil, (0, 0), circle_pil)
    bg.paste(circle_pil, (bg.width - circle_pil.width, 0), circle_pil)
    circle_pil.close()

    # 画一个正方形
    draw = ImageDraw.Draw(bg, mode='RGBA')
    draw.rectangle(
        (
            int(circle_pil.width / 2),
            0,
            bg.width - int(circle_pil.width / 2),
            bg.height
        ), fill=bg_color, outline=None, width=0
    )

    bg = bg.resize((width, height), 1)
    return bg


if __name__ == '__main__':
    fun_圆角矩形背景(width=900, height=240, bg_color=(18, 210, 172)).show()
