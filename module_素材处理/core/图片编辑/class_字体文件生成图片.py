from typing import Literal
from PIL import ImageFont, Image, ImageDraw

Direction = Literal['ltr', 'ttb']


class FontToPIL:
    def __init__(self, font_path: str, text: str, direction: Direction):
        self.font_path = font_path
        self.text = text
        self.direction = direction

    font_size = 480
    font_color = (255, 255, 255)
    background = (255, 255, 255, 0)

    def fun_单个文字生成图片(self):
        true_font = ImageFont.truetype(font=self.font_path, size=self.font_size)
        bbox = true_font.getbbox(self.text, direction=self.direction)

        bg = Image.new('RGBA', (bbox[2], bbox[3]), self.background)
        draw = ImageDraw.Draw(bg)
        draw.text(
            (0, 0), text=self.text, fill=self.font_color, font=true_font, direction=self.direction
        )

        return bg


if __name__ == '__main__':
    ftp = FontToPIL(
        font_path=r'E:\小夕素材\9000-9999\9261\9261\100_199\小夕素材(101).otf',
        text='花落无声',
        direction='ttb'
    )
    fbg = ftp.fun_单个文字生成图片()
    fbg.show()
