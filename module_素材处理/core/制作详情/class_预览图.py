from functools import cached_property
from pathlib import Path
from typing import List

from PIL import Image

from module_素材处理.core.图片编辑.class_picedit import PICEdit
from module_素材处理.core.setting import MATERIAL_FILE_SUFFIX
from module_素材处理.core.素材文件夹功能.fun_指定遍历 import fun_指定遍历
from module_素材处理.core.setting import PIC_EDIT_IMG


class XQPreviewPic:
    def __init__(self, img_list: List[Path], material_path: Path, tb_name: str):
        self.img_list = img_list
        self.material_path = material_path
        self.tb_name = tb_name

        self.width = 1500
        self.gutter = 30

    @cached_property
    def fun_单行实际图片宽度(self):
        return int(self.width - (self.gutter * 2))

    def fun_单行小图片(self, img: Path):
        im = Image.open(img.as_posix()).convert('RGBA')
        ori_width = im.width
        ori_height = im.height

        height = int(self.fun_单行实际图片宽度 / (im.width / im.height))
        im = im.resize((self.fun_单行实际图片宽度, height), 1)
        im = PICEdit.fun_图片圆角(im, 20).main()
        im.ori_width = ori_width
        im.ori_height = ori_height

        return im

    def fun_查找对应源文件(self, img: Path):
        for in_file in fun_指定遍历(self.material_path, MATERIAL_FILE_SUFFIX):
            if in_file.stem == img.stem:
                return in_file

        return None

    @staticmethod
    def fun_制作信息(stem: str, size_info: str):
        stem_pil = PICEdit.fun_单行文字(text=stem.upper(), font_weight='r', font_size=46, text_color=(120, 120, 120),
                                        bg_color=(255, 255, 255)).main()
        size_info = PICEdit.fun_单行文字(text=size_info.upper(), font_weight='r', font_size=38,
                                         text_color=(120, 120, 120),
                                         bg_color=(255, 255, 255)).main()
        bg_width = max([stem_pil.width, size_info.width])
        bg_height = sum([stem_pil.height, size_info.height]) + 260
        bg = Image.new('RGBA', (bg_width, bg_height), (255, 255, 255))

        top = 60
        for pil in [stem_pil, size_info]:
            left = int((bg.width - pil.width) / 2)
            bg.paste(pil, (left, top), pil)
            top += pil.height + 20
            pil.close()

        return bg

    @staticmethod
    def fun_图片和信息粘贴到一起(small_im: Image.Image, info_pil: Image.Image):
        bg_width = small_im.width
        bg_height = sum([small_im.height, info_pil.height])
        bg = Image.new('RGBA', (bg_width, bg_height), (255, 255, 255))

        top = 0
        for pil in [small_im, info_pil]:
            left = int((bg.width - pil.width) / 2)
            bg.paste(pil, (left, top), pil)
            top += pil.height
        return bg

    @cached_property
    def fun_水印图片(self):
        water_mark = Image.open(
            (PIC_EDIT_IMG / self.tb_name / '蜘蛛网水印.png').as_posix()
        )
        water_mark.thumbnail((1500, 9999))
        return water_mark

    def fun_单个图片添加水印(self, small_im: Image.Image):
        water_mark = self.fun_水印图片
        small_im.paste(water_mark, (
            int((small_im.width - water_mark.width) / 2),
            int((small_im.height - water_mark.height) / 2)
        ), water_mark)
        return small_im

    def main(self):
        all_pil = []
        for num, img in enumerate(self.img_list):
            small_im = self.fun_单行小图片(img)
            if num % 2 != 0:
                small_im = self.fun_单个图片添加水印(small_im)

            ma_file = self.fun_查找对应源文件(img)
            if ma_file is not None:
                if ma_file.suffix.lower() not in ['.ai', '.eps']:
                    info_pil = self.fun_制作信息(ma_file.name, f'{small_im.ori_width}*{small_im.ori_height}(PX)')
                else:
                    info_pil = self.fun_制作信息(ma_file.name, f'矢量设计素材')

                small_im = self.fun_图片和信息粘贴到一起(small_im, info_pil)

            all_pil.append(small_im)

        left = self.gutter
        top = 0
        bg = Image.new('RGBA', (self.width, sum([pil.height+self.gutter for pil in all_pil])), (255, 255, 255))
        for pil in all_pil:
            bg.paste(pil, (left, top), pil)
            top += pil.height + self.gutter
            pil.close()

        return bg


if __name__ == '__main__':
    from core.素材文件夹功能.fun_指定遍历 import fun_指定遍历

    XQPreviewPic(
        img_list=fun_指定遍历(Path(r'G:\饭桶设计\1000-1999\1023\预览图'), ['.png']),
        material_path=Path(r'G:\饭桶设计\1000-1999\1023\1023')
    ).main().show()
