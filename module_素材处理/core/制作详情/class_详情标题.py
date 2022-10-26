from functools import cached_property

from PIL import Image

from module_素材处理.core.图片编辑.fun_单行文字转PIL import TextToPIL


class XQTitlePic:
    def __init__(self, title: str, sec_title: str):
        self.title = title
        self.sec_title = sec_title

    @cached_property
    def title_pil(self):
        return TextToPIL(text=self.title, text_color=(90, 90, 90), bg_color=(255, 255, 255), font_weight='m',
                         font_size=60).main()

    @cached_property
    def sec_title_pil(self):
        return TextToPIL(text=self.sec_title, text_color=(90, 90, 90), bg_color=(255, 255, 255), font_weight='m',
                         font_size=30).main()

    def main(self):
        bg_width = 1500

        mt = 300
        gutter = 20
        mb = 80

        bg_height = mt + sum([self.title_pil.height, self.sec_title_pil.height]) + gutter + mb
        bg = Image.new('RGBA', (bg_width, bg_height), (255, 255, 255))

        top = mt
        for pil in [self.title_pil, self.sec_title_pil]:
            left = int((bg.width - pil.width) / 2)
            bg.paste(pil, (left, top), pil)
            top += pil.height + gutter
            pil.close()

        return bg


if __name__ == '__main__':
    XQTitlePic(
        title='素材信息', sec_title='购买前请务必仔细阅读购物须知'
    ).main().show()
