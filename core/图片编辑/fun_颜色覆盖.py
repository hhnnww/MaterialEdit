from typing import Tuple

from PIL import Image


def fun_颜色覆盖(img: Image.Image, color: Tuple[int]) -> Image.Image:
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    for x in range(img.width):
        for y in range(img.height):
            _, _, _, transparency = img.getpixel((x, y))
            img.putpixel((x, y), (color[0], color[1], color[2], transparency))

    return img
