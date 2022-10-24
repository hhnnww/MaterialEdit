from typing import List
from pathlib import Path
from PIL import Image

from core.setting import PIC_EDIT_IMG
from core.图片编辑.class_picedit import PICEdit


class STHeiJingStyle:
    def __init__(self, layout_bg: Image.Image, title: str, material_format_list: List[str], tb_name: str):
        self.layout_bg = layout_bg
        self.title = title
        self.material_format_list = material_format_list
        self.logo_pil = Image.open(
            (Path(__file__).parent / 'IMAGE' / tb_name / 'logo.png').as_posix()
        )

    circle_color_list = dict(
        psd=dict(
            text_color=(49, 168, 255),
            border_color=(49, 168, 255),
            bg_color=(0, 30, 54)
        ),
        ai=dict(
            text_color=(255, 154, 0),
            border_color=(255, 154, 0),
            bg_color=(51, 0, 0)
        ),
        ppt=dict(
            text_color=(255, 255, 255),
            border_color=(255, 143, 106),
            bg_color=(187, 53, 24)
        )
    )

    def fun_制作横条背景(self):
        bg = Image.new('RGBA', (1500, 200), (0, 0, 0))
        bg = PICEdit.fun_图片圆角(bg, 180, None, angle=['lb', 'rb']).main()

        title_pil = PICEdit.fun_单行文字(self.title, 'm', 100, (255, 255, 255), (0, 0, 0)).main()
        left = 80
        top = int((bg.height - title_pil.height) / 2)
        bg.paste(title_pil, (left, top), title_pil)
        title_pil.close()

        return bg

    def fun_单个格式圆圈(self, material_format):
        material_format = material_format.lower()
        bg_circle = Image.open((PIC_EDIT_IMG / '圆角背景.png').as_posix())
        prospect_circle = bg_circle.copy()

        bg_circle.thumbnail((166, 166), resample=1)
        bg_circle = PICEdit.fun_颜色覆盖(bg_circle, self.circle_color_list.get(material_format).get('border_color'))

        prospect_circle.thumbnail((150, 150), resample=1)
        prospect_circle = PICEdit.fun_颜色覆盖(prospect_circle,
                                               self.circle_color_list.get(material_format).get('bg_color'))

        left = int((bg_circle.width - prospect_circle.width) / 2)
        top = int((bg_circle.height - prospect_circle.height) / 2)
        bg_circle.paste(prospect_circle, (left, top), prospect_circle)
        prospect_circle.close()

        title_pil = PICEdit.fun_单行文字(material_format.upper(), 'h', 46,
                                         self.circle_color_list.get(material_format).get('text_color'),
                                         self.circle_color_list.get(material_format).get('bg_color')).main()

        left = int((bg_circle.width - title_pil.width) / 2)
        top = int((bg_circle.height - title_pil.height) / 2)
        bg_circle.paste(title_pil, (left, top), title_pil)
        title_pil.close()

        return bg_circle

    def main(self):
        bg = Image.new('RGBA', (1500, 1500), (255, 255, 255))
        bg.paste(self.layout_bg, (0, 0))
        self.layout_bg.close()

        title_bg = self.fun_制作横条背景()
        bg.paste(title_bg, (0, 1300))
        title_bg.close()

        right = 100
        gutter = 30
        ma_pil_list = [self.fun_单个格式圆圈(ma) for ma in self.material_format_list]

        all_gutter = (len(ma_pil_list) - 1) * gutter
        left = bg.width - (sum([pil.width for pil in ma_pil_list]) + all_gutter + right)
        top = int(1300 - (ma_pil_list[0].height / 2))
        for ma_pil in ma_pil_list:
            bg.paste(ma_pil, (left, top), ma_pil)
            left += ma_pil.width + gutter
            ma_pil.close()

        self.logo_pil.thumbnail((180, 180))
        bg.paste(self.logo_pil, (60, 60), self.logo_pil)
        return bg


if __name__ == '__main__':
    STHeiJingStyle(
        Image.new('RGBA', (1500, 1300), (255, 255, 255)),
        '2023春节兔年海报',
        ['PSD', 'ai'],
        'paopao'
    ).main().show()
