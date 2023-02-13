from functools import cached_property
from typing import List

from PIL import Image

from module_素材处理.core.setting import IMG_PATH
from module_素材处理.core.图片编辑.class_picedit import PICEdit


class STHeiJingStyle:
    def __init__(self, layout_bg: Image.Image, title: str, material_format_list: List[str], tb_name: str,
                 material_id: str):
        self.layout_bg = layout_bg
        self.title = title
        self.material_format_list = material_format_list
        self.tb_name = tb_name
        self.material_id = material_id

        # self.logo_pil = Image.open(
        #     (PIC_EDIT_IMG / tb_name / 'logo.png').as_posix()
        # )

    circle_color_list = dict(
        psd=dict(
            text_color=(49, 168, 255),
            border_color=(49, 168, 255),
            bg_color=(0, 30, 54)
        ),
        png=dict(
            text_color=(49, 168, 255),
            border_color=(49, 168, 255),
            bg_color=(0, 30, 54)
        ),
        ai=dict(
            text_color=(255, 154, 0),
            border_color=(255, 154, 0),
            bg_color=(51, 0, 0)
        ),
        svg=dict(
            text_color=(255, 154, 0),
            border_color=(255, 154, 0),
            bg_color=(51, 0, 0)
        ),
        ppt=dict(
            text_color=(255, 255, 255),
            border_color=(255, 143, 106),
            bg_color=(187, 53, 24)
        ),
        pptx=dict(
            text_color=(255, 255, 255),
            border_color=(255, 143, 106),
            bg_color=(187, 53, 24)
        ),
        otf=dict(
            text_color=(255, 255, 255),
            border_color=(255, 143, 106),
            bg_color=(187, 53, 24)
        ),
        ttf=dict(
            text_color=(255, 255, 255),
            border_color=(255, 143, 106),
            bg_color=(187, 53, 24)
        ),
        pro=dict(
            text_color=(255, 255, 255),
            border_color=(255, 143, 106),
            bg_color=(187, 53, 24)
        )

    )

    def fun_制作横条背景(self):
        bg = Image.new('RGBA', (1500, 200), (0, 0, 0))
        bg = PICEdit.fun_图片圆角(bg, 180, None, angle=['lb', 'rb']).main()

        title_pil = PICEdit.fun_单行文字(self.title, 'm', 95, (255, 255, 255), (0, 0, 0)).main()
        left = 80
        top = int((bg.height - title_pil.height) / 2)
        bg.paste(title_pil, (left, top), title_pil)
        title_pil.close()

        return bg

    def fun_单个格式圆圈(self, material_format):
        material_format = material_format.lower()

        title_pil = PICEdit.fun_单行文字(material_format.upper(), 'h', 200,
                                         self.circle_color_list.get(material_format).get('text_color'),
                                         self.circle_color_list.get(material_format).get('bg_color')).main()

        bg_circle = Image.open((IMG_PATH / '圆角背景.png').as_posix())
        prospect_circle = bg_circle.copy()

        if len(material_format) == 2:
            oneline_size = int(title_pil.width * 2.5)
        elif len(material_format) == 3:
            oneline_size = int(title_pil.width * 1.8)
        else:
            oneline_size = int(title_pil.width * 1.5)

        bg_circle = bg_circle.resize(
            (oneline_size, oneline_size),
            resample=1
        )
        bg_circle = PICEdit.fun_颜色覆盖(bg_circle, self.circle_color_list.get(material_format).get('border_color'))

        prospect_circle = prospect_circle.resize((
            int(bg_circle.width * 0.89), int(bg_circle.width * 0.89)
        ), resample=1)
        prospect_circle = PICEdit.fun_颜色覆盖(prospect_circle,
                                               self.circle_color_list.get(material_format).get('bg_color'))

        left = int((bg_circle.width - prospect_circle.width) / 2)
        top = int((bg_circle.height - prospect_circle.height) / 2)
        bg_circle.paste(prospect_circle, (left, top), prospect_circle)
        prospect_circle.close()

        left = int((bg_circle.width - title_pil.width) / 2)
        top = int((bg_circle.height - title_pil.height) / 2)
        bg_circle.paste(title_pil, (left, top), title_pil)
        title_pil.close()
        bg_circle.thumbnail((180, 180), 1)
        return bg_circle

    @cached_property
    def fun_素材ID(self):
        id_pil = PICEdit.fun_单行文字(text='ID:' + self.material_id, font_weight='h', font_size=300,
                                      text_color=(255, 255, 255),
                                      bg_color=(0, 0, 0)).main()
        bg = Image.new('RGBA', (
            int(id_pil.width * 1.4), int(id_pil.height * 2.4)
        ), (0, 0, 0))
        bg = PICEdit.fun_图片圆角(bg, radius=500, border_color=None).main()
        bg.paste(id_pil, (
            int((bg.width - id_pil.width) / 2), int((bg.height - id_pil.height) / 2)
        ), id_pil)
        id_pil.close()
        bg.thumbnail((100, 100), 1)
        return bg

    def main(self):
        bg = Image.new('RGBA', (1500, 1500), (255, 255, 255))
        bg.paste(self.layout_bg, (0, 0))
        self.layout_bg.close()

        title_bg = self.fun_制作横条背景()
        bg.paste(title_bg, (0, 1300))
        title_bg.close()

        right = 100
        gutter = 30
        ma_pil_list = [self.fun_单个格式圆圈(ma) for ma in self.material_format_list if ma.lower() not in ['eps']]

        all_gutter = (len(ma_pil_list) - 1) * gutter
        left = bg.width - (sum([pil.width for pil in ma_pil_list]) + all_gutter + right)
        top = int(1300 - (ma_pil_list[0].height / 2))
        for ma_pil in ma_pil_list:
            bg.paste(ma_pil, (left, top), ma_pil)
            left += ma_pil.width + gutter
            ma_pil.close()

        # self.logo_pil.thumbnail((180, 180))
        # bg.paste(self.logo_pil, (60, 60), self.logo_pil)
        bg.paste(self.fun_素材ID, (40, 40), self.fun_素材ID)

        return bg


if __name__ == '__main__':
    STHeiJingStyle(
        Image.new('RGBA', (1500, 1300), (255, 255, 255)),
        '2023春节兔年海报',
        ['PSD', 'ai', 'pptx'],
        '泡泡猫素材', '3345'
    ).main().show()
