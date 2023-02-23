from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import List

from PIL import Image
from tqdm import tqdm

from module_素材处理.core.setting import IMG_PATH
from module_素材处理.core.setting import MATERIAL_FILE_SUFFIX
from module_素材处理.core.setting import TEXT_COLOR
from module_素材处理.core.图片编辑.class_picedit import PICEdit
from module_素材处理.core.素材文件夹功能.fun_指定遍历 import fun_指定遍历


@dataclass
class IMGType:
    path: Path
    width: int
    height: int
    ratio: float


class XQMakePIC:
    def __init__(self,
                 img_list: List[Path],
                 single_pic_num: float,
                 material_path: Path,
                 has_material_info: bool,
                 tb_name: str,
                 pic_water_market: bool,
                 ):
        self.img_list = img_list
        self.single_pic_num = single_pic_num
        self.material_path = material_path
        self.has_material_info = has_material_info
        self.tb_name = tb_name
        self.pic_water_market = pic_water_market

        self.xq_width = 1500
        self.gutter = 30

    @cached_property
    def fun_构建列表(self):
        pil_list = []
        for img_path in self.img_list:
            try:
                with Image.open(img_path.as_posix()) as im:
                    pil_list.append(
                        IMGType(path=img_path, width=im.width, height=im.height, ratio=im.width / im.height)
                    )
            except:
                pass

        return pil_list

    @cached_property
    def fun_组合列表(self):
        comb_list = []
        line_comb = []
        large_pic = 10
        for num, img_type in enumerate(self.fun_构建列表):
            if (num == 0 or num > large_pic) and img_type.ratio > 1.3:
                comb_list.append([img_type])
                large_pic += 10

            else:
                line_comb.append(img_type)

                # 选择单排数量
                line_sum_ratio = sum([in_img.ratio for in_img in line_comb])
                if len(line_comb) == self.single_pic_num or line_sum_ratio >= 5:
                    comb_list.append(line_comb.copy())
                    line_comb = []

            # 如果到了最后一行还有图片
            if num == len(self.fun_构建列表) - 1:
                if len(line_comb) > 0:
                    comb_list.append(line_comb.copy())

        return comb_list

    @cached_property
    def fun_所有源文件(self):
        return fun_指定遍历(self.material_path, MATERIAL_FILE_SUFFIX)

    def fun_查找源文件(self, img_path: Path):
        for in_file in self.fun_所有源文件:
            if in_file.stem == img_path.stem:
                return in_file

        return None

    @staticmethod
    def fun_制作信息(stem: str, size_info: str):
        stem_pil = PICEdit.fun_单行文字(text=stem.upper(), font_weight='l', font_size=40, text_color=TEXT_COLOR,
                                        bg_color=(255, 255, 255)).main()
        size_info = PICEdit.fun_单行文字(text=size_info.upper(), font_weight='l', font_size=32,
                                         text_color=TEXT_COLOR,
                                         bg_color=(255, 255, 255)).main()

        bg_width = max([stem_pil.width, size_info.width])
        bg_height = sum([stem_pil.height, size_info.height]) + 260
        bg = Image.new('RGBA', (bg_width, bg_height), (255, 255, 255))

        top = 40
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

        info_pil.thumbnail((small_im.width - 40, 99999), 1)
        top = 0
        for pil in [small_im, info_pil]:
            left = int((bg.width - pil.width) / 2)
            bg.paste(pil, (left, top), pil)
            top += pil.height
            pil.close()

        return bg

    def fun_制作单行(self, line_comb_list: List[IMGType], line_num: int):
        line_actual_width = self.xq_width - ((len(line_comb_list) + 1) * self.gutter)
        line_actual_height = int(line_actual_width / sum([img_type.ratio for img_type in line_comb_list]))

        line_pil_list = []
        mt = 0
        for num, img_type in enumerate(line_comb_list):
            small_im_width = int(line_actual_height * img_type.ratio)
            small_im = Image.open(img_type.path.as_posix()).convert('RGBA')
            small_im = small_im.resize((small_im_width, line_actual_height), resample=1)
            small_im = PICEdit.fun_图片圆角(small_im, 20).main()

            if self.has_material_info is True:
                material_file = self.fun_查找源文件(img_type.path)
                if material_file is not None:
                    if material_file.suffix.lower() in ['.psd', '.psb']:
                        size = f'{img_type.width}*{img_type.height}(PX)'
                    elif material_file.suffix.lower() in ['.ai', '.eps']:
                        size = f'矢量设计素材'
                    else:
                        size = f' '

                    small_im_info_pil = self.fun_制作信息(stem=material_file.name.upper(), size_info=size)
                    mt = small_im_info_pil.height
                    small_im = self.fun_图片和信息粘贴到一起(small_im, small_im_info_pil)

            line_pil_list.append(small_im)

        bg = Image.new('RGBA', (self.xq_width, max([pil.height for pil in line_pil_list]) + self.gutter),
                       (255, 255, 255))

        left, top = self.gutter, 0
        for pil in line_pil_list:
            bg.paste(pil, (left, top), pil)
            left += self.gutter + pil.width
            pil.close()

        if line_num % 2 != 0 and self.pic_water_market is True:
            bg = self.fun_添加水印(bg, mt=mt)

        return bg

    def fun_添加水印(self, small_im: Image.Image, mt: int):
        water_pil = Image.open(
            (IMG_PATH / self.tb_name / '蜘蛛网水印.png').as_posix()
        )
        water_pil.thumbnail((1500, 9999), 1)
        left = int((small_im.width - water_pil.width) / 2)
        top = int(((small_im.height - mt) - water_pil.height) / 2)

        small_im.paste(water_pil, (left, top), water_pil)
        water_pil.close()

        return small_im

    def main(self):
        pil_list = []
        line_num = 0
        for line_comb in tqdm(self.fun_组合列表, desc='制作详情', ncols=100):
            line_pil = self.fun_制作单行(line_comb, line_num)
            pil_list.append(line_pil)
            line_num += 1

        xq_height = sum([pil.height for pil in pil_list])
        bg = Image.new('RGBA', (self.xq_width, xq_height), (255, 255, 255))

        left, top = 0, 0
        for pil in pil_list:
            bg.paste(pil, (left, top), pil)
            top += pil.height
            pil.close()

        return bg
