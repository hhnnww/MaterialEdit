import string

from PIL import Image
from PIL import ImageChops
from PIL import ImageDraw
from PIL import ImageFont

from module_素材处理.core.setting import FONT_PATH


def in_is_en(text: str) -> bool:
    if text in string.printable:
        return True
    else:
        return False


def fun_T500标题(title: str):
    cn_fnt = FONT_PATH / '思源黑体' / 'SourceHanSansCN-Heavy.otf'
    en_fnt = FONT_PATH / 'Lato' / 'lato-v23-latin-900.ttf'

    size = 150

    cn_font = ImageFont.truetype(cn_fnt.as_posix(), size)
    en_font = ImageFont.truetype(en_fnt.as_posix(), int(size * 1.2))

    max_w, max_h = 0, 0

    for text in title:
        if in_is_en(text):
            en_size = en_font.getsize(text)
            max_w += en_size[0]
            if en_size[1] > max_h:
                max_h = en_size[1]
        else:
            cn_size = list(cn_font.getsize(text))
            max_w += cn_size[0]
            if cn_size[1] > max_h:
                max_h = cn_size[1]

    bg = Image.new('RGB', (max_w, max_h), (255, 205, 85))
    draw = ImageDraw.Draw(bg)

    left, top = 0, 0
    for text in title:
        if in_is_en(text):
            en_size = en_font.getsize(text)
            top = int((bg.height - en_size[1]) / 2)
            draw.text((left, top), text, font=en_font, fill=(0, 0, 0))
            left += en_size[0]
        else:
            cn_size = list(cn_font.getsize(text))
            cn_size[1] = cn_size[1]
            top = int((bg.height - cn_size[1]) / 2)
            draw.text((left, top), text, font=cn_font, fill=(0, 0, 0))
            left += cn_size[0]

    new_bg = Image.new('RGB', bg.size, (255, 205, 85))
    diff = ImageChops.difference(bg, new_bg)
    bbox = diff.getbbox()

    if bbox:
        bg = bg.crop(bbox)
    return bg


if __name__ == '__main__':
    fun_T500标题('200套 兔年海报').show()
