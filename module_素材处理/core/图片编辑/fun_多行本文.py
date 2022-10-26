from typing import Literal, Tuple

from PIL import Image

from module_素材处理.core.图片编辑.fun_单行文字转PIL import TextToPIL
from module_素材处理.core.图片编辑.fun_边框删除 import DelPILBorder


def fun_多行本文(text: str, line_width: int, font_weight: Literal['l', 'r', 'm', 'b', 'h'], font_size: int,
                 text_colr: Tuple[str], bg_color: Tuple[str], line_height: float) -> Image.Image:
    text_list = [text[i:i + line_width] for i in range(0, len(text), line_width)]
    all_pil = [TextToPIL(text=line, font_weight=font_weight, font_size=font_size, text_color=text_colr,
                         bg_color=bg_color).main() for line in text_list]

    bg_height = int(sum([pil.height * line_height for pil in all_pil]))
    bg_width = int(max([pil.width for pil in all_pil]))

    bg = Image.new('RGBA', (bg_width, bg_height), bg_color)
    left, top = 0, 0
    for pil in all_pil:
        bg.paste(pil, (left, top), pil)
        top += int(pil.height * line_height)
        pil.close()

    bg = DelPILBorder(bg, None).main()

    return bg


if __name__ == '__main__':
    fun_多行本文(
        text='本店是设计师专用素材，如果您不是设计师，请不要购买，不要购买，本店不提供任何使用教程。',
        line_width=30,
        font_weight='r',
        font_size=24,
        text_colr=(90, 90, 90),
        bg_color=(255, 255, 255),
        line_height=1.3
    ).show()
