from typing import Optional, Tuple

from PIL import Image, ImageDraw

from core.setting import *


class PICToCircle:
    def __init__(self, img: Image.Image, radius: int, border_color: Optional[Tuple[int]] = (240, 240, 240),
                 angle=None):

        if angle is None:
            angle = ['lt', 'rt', 'lb', 'rb']
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        self.img = img
        self.radius = radius
        self.border_color = border_color
        self.circle_pil = Image.open((PIC_EDIT_IMG / '圆角背景.png').as_posix())
        self.circle_pil.thumbnail((radius, radius), resample=Image.ANTIALIAS)
        self.angle = angle

        self.use_transparent = 30

    def main(self):
        if self.border_color is not None:
            draw = ImageDraw.Draw(self.img)
            draw.line(((0, 0), (0, self.img.height)), fill=self.border_color, width=1)
            draw.line(((0, 0), (self.img.width, 0)), fill=self.border_color, width=1)
            draw.line(((self.img.width - 1, 0), (self.img.width - 1, self.img.height - 1)), fill=self.border_color,
                      width=1)
            draw.line(((0, self.img.height - 1), (self.img.width, self.img.height - 1)), fill=self.border_color,
                      width=1)

        # 左上角
        if 'lt' in self.angle:
            for x in range(int(self.radius / 2)):
                for y in range(int(self.radius / 2)):
                    circle_current_transparent = self.circle_pil.getpixel((x, y))[-1]
                    if circle_current_transparent < self.use_transparent:
                        r, g, b, a = self.img.getpixel((x, y))
                        self.img.putpixel((x, y), (r, g, b, circle_current_transparent))

        if 'rt' in self.angle:
            # 右上角
            for x in range(int(self.radius / 2)):
                for y in range(int(self.radius / 2)):
                    circle_current_transparent = self.circle_pil.getpixel((int(x + (self.radius / 2)), y))[-1]
                    if circle_current_transparent < self.use_transparent:
                        left = int(self.img.width - (self.radius / 2)) + x
                        top = y
                        r, g, b, a = self.img.getpixel((left, top))
                        self.img.putpixel((left, top), (r, g, b, circle_current_transparent))

        if 'lb' in self.angle:
            # 左下角
            for x in range(int(self.radius / 2)):
                for y in range(int(self.radius / 2)):
                    circle_current_transparent = self.circle_pil.getpixel(
                        (x, int((self.radius / 2) + y))
                    )[-1]
                    if circle_current_transparent < self.use_transparent:
                        top = int(self.img.height - (self.radius / 2)) + y
                        r, g, b, a = self.img.getpixel((x, top))
                        self.img.putpixel((x, top), (r, g, b, circle_current_transparent))

        if 'rb' in self.angle:
            # 右下角
            for x in range(int(self.radius / 2)):
                for y in range(int(self.radius / 2)):
                    circle_current_transparent = self.circle_pil.getpixel(
                        (int((self.radius / 2) + x), int((self.radius / 2) + y))
                    )[-1]
                    if circle_current_transparent < self.use_transparent:
                        left = int(self.img.width - (self.radius / 2)) + x
                        top = int(self.img.height - (self.radius / 2)) + y
                        r, g, b, a = self.img.getpixel((left, top))
                        self.img.putpixel((left, top), (r, g, b, circle_current_transparent))

        self.circle_pil.close()

        return self.img


if __name__ == '__main__':
    PICToCircle(
        img=Image.open(r'C:\Users\wuweihua\Desktop\qrcode.png'), radius=180
    ).main().show()
