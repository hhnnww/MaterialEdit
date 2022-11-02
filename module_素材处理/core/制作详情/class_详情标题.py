from functools import cached_property

from PIL import Image

from module_素材处理.core.setting import TEXT_COLOR
from module_素材处理.core.图片编辑.class_picedit import PICEdit
from module_素材处理.core.图片编辑.fun_单行文字转PIL import TextToPIL


class XQTitlePic:
    def __init__(self, title: str, sec_title: str):
        self.title = title
        self.sec_title = sec_title

        self.text_color = TEXT_COLOR

    @cached_property
    def title_pil(self):
        return TextToPIL(text=self.title, text_color=self.text_color, bg_color=(255, 255, 255, 0), font_weight='b',
                         font_size=60).main()

    @cached_property
    def sec_title_pil(self):
        return TextToPIL(text=self.sec_title, text_color=self.text_color, bg_color=(255, 255, 255, 0), font_weight='r',
                         font_size=30).main()

    @cached_property
    def circle_bg(self):
        circle_pil = PICEdit.fun_圆角矩形背景(width=self.title_pil.width + 10, height=20, bg_color=(245, 199, 87))
        for x in range(circle_pil.width):
            for y in range(circle_pil.height):
                c1, c2, c3, transparency = circle_pil.getpixel((x, y))
                circle_pil.putpixel((x, y), (c1, c2, c3, int(transparency)))

        return circle_pil

    def main(self):
        bg_width = 1500

        mt = 300
        gutter = 30
        mb = 100

        bg_height = mt + sum([self.title_pil.height, self.sec_title_pil.height]) + gutter + mb
        bg = Image.new('RGBA', (bg_width, bg_height), (255, 255, 255))

        bg.paste(
            self.circle_bg,
            (
                int((bg.width - self.circle_bg.width) / 2),
                300 + self.title_pil.height - 10
            ),
            self.circle_bg
        )

        top = mt
        for pil in [self.title_pil, self.sec_title_pil]:
            left = int((bg.width - pil.width) / 2)
            bg.paste(pil, (left, top), pil)
            top += pil.height + gutter
            pil.close()

        return bg


if __name__ == '__main__':
    XQTitlePic(
        title='效果图', sec_title='此效果图素材内不提供'
    ).main().show()
