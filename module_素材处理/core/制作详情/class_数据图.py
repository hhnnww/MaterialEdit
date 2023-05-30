from typing import List, Tuple

from PIL import Image

from module_素材处理.core.图片编辑 import PICEdit


class XQInfoPic:
    def __init__(self, text_list: List[Tuple[str, str]]):
        self.text_list = text_list

    @staticmethod
    def fun_单行制作(text_item: Tuple[str], num: int):
        bg_color = (255, 255, 255)
        if num % 2 != 0:
            bg_color = (250, 250, 250)

        all_pil = [
            PICEdit.fun_多行本文(text=text, line_height=1.35, font_weight='l', font_size=40, text_colr=(90, 90, 120),
                                 bg_color=bg_color, line_width=22) for text in text_item]

        width = 720 * 2
        gutter = 30 * 2
        height = int(max([pil.height for pil in all_pil]) + (gutter * 2))
        top = gutter

        left = 50 * 2
        left_2 = 220 * 2

        bg = Image.new('RGBA', (width, height), bg_color)
        bg.paste(all_pil[0], (left, top), all_pil[0])
        bg.paste(all_pil[1], (left_2, top), all_pil[1])
        all_pil[0].close()
        all_pil[1].close()

        return bg

    def main(self):
        all_pil = [self.fun_单行制作(text_item, num) for num, text_item in enumerate(self.text_list)]
        width = 720 * 2
        height = sum([pil.height for pil in all_pil])
        bg = Image.new('RGBA', (width, height), (255, 255, 255))
        left = 0
        top = 0
        for pil in all_pil:
            bg.paste(pil, (left, top), pil)
            top += pil.height
            pil.close()

        bg = PICEdit.fun_图片圆角(bg, radius=20).main()
        new_bg = Image.new('RGBA', (1500, bg.height + 60), (255, 255, 255))
        new_bg.paste(bg, (30, 30), bg)
        bg.close()
        return new_bg


if __name__ == '__main__':
    XQInfoPic(
        [
            ('素材标题', '2023年兔年海报'),
            ('素材数量', '23个PSD文件'),
            ('素材尺寸', '234.56 MB'),
            ('购买须知', '本店均为设计师专用素材，如果您不是设计师，请勿购买，本店不提供任何使用教程。')
        ]
    ).main().show()
