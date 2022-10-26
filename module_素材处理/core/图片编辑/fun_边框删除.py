from functools import cached_property
from typing import Tuple, Optional

from PIL import Image


class DelPILBorder:
    def __init__(self, img: Image.Image, border_color: Optional[Tuple[int]]):
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        self.img = img
        self.border_color = border_color

    @cached_property
    def fun_边框颜色(self):
        if self.border_color is None:
            return self.img.getpixel((0, 0))

        return self.border_color

    @cached_property
    def left(self):
        for left in range(0, self.img.width):
            for top in range(0, self.img.height):
                if self.img.getpixel((left, top)) != self.fun_边框颜色:
                    if left > 0:
                        left -= 1
                    return left

    @cached_property
    def upper(self):
        for top in range(0, self.img.height):
            for left in range(0, self.img.width):
                if self.img.getpixel((left, top)) != self.fun_边框颜色:
                    if top > 1:
                        top -= 1
                    return top

    @cached_property
    def right(self):
        for right in range(self.img.width - 1, 0, -1):
            for top in range(0, self.img.height):
                if self.img.getpixel((right, top)) != self.fun_边框颜色:
                    if right < self.img.width:
                        right += 1
                    return right

    @cached_property
    def bottom(self):
        for bottom in range(self.img.height - 1, 0, -1):
            for left in range(0, self.img.width):
                if self.img.getpixel((left, bottom)) != self.fun_边框颜色:
                    if bottom < self.img.height:
                        bottom += 1
                    return bottom

    def main(self) -> Image.Image:
        bbox = (self.left, self.upper, self.right, self.bottom)
        img = self.img.crop(bbox)
        return img


if __name__ == '__main__':
    DelPILBorder(
        Image.open(r'C:\Users\wuweihua\Desktop\微信图片_20221022204632.jpg'), None
    ).main().show()
