import random
from functools import cached_property
from typing import List, Tuple

from PIL import Image

from module_素材处理.core.制作首图.布局.class_type import ComList
from module_素材处理.core.图片编辑.class_picedit import PICEdit

Image.MAX_IMAGE_PIXELS = None


class SmallSizeModel:
    # 单行小图片宽度自适应，高度一致
    AUTO = 1

    # 小图片宽高全部自适应
    ALL_AUTO = 2

    # 小图片宽高完全一致
    AVERAGE = 3


class STMake:
    def __init__(self, st_list: List[ComList], st_width: int, st_height: int, gutter: int,
                 bg_color: Tuple[int, int, int],
                 small_pic_size_mode: int, crop_model: str):
        self.st_list = st_list

        self.st_list.sort(key=lambda k: len(k.img_list))

        self.st_width = st_width
        self.st_height = st_height
        self.gutter = gutter
        self.bg_color = bg_color
        self.st_row = len(self.st_list)
        self.small_pic_size_mode = small_pic_size_mode
        self.crop_model = crop_model
        self.circle_radius = 20

    def fun_制作小图片(self, img: Image.Image, small_width: int, small_height: int, num: int) -> Image.Image:
        if num % 2 == 0:
            img = PICEdit.fun_图片裁剪(img, small_width + 1, small_height, direction=self.crop_model)
        else:
            img = PICEdit.fun_图片裁剪(img, small_width, small_height, direction=self.crop_model)
        if self.gutter > 0:
            img = PICEdit.fun_图片圆角(img, self.circle_radius, (240, 240, 240)).main()
        return img

    def fun_自适应单行(self, com_list: ComList):
        """单行高度均分，小图宽度自适应"""
        pic_width = int(self.st_width - ((len(com_list.img_list) + 1) * self.gutter))
        line_height = int((self.st_height - ((self.st_row + 1) * self.gutter)) / self.st_row)

        bg = Image.new('RGBA', (self.st_width, line_height), self.bg_color)
        left = self.gutter

        img_list = list(com_list.img_list)
        random.shuffle(img_list)

        for num, img_path in enumerate(img_list):
            with Image.open(img_path.img_path).convert('RGBA') as im:
                small_im_width = int(pic_width * (img_path.ratio / com_list.ratio))
                small_im = self.fun_制作小图片(im, small_im_width, line_height, num)
                bg.paste(small_im, (left, 0), small_im)
                left += small_im.width + self.gutter
                small_im.close()
        return bg

    @cached_property
    def fun_计算原始高度(self):
        ori_height = 0
        for comb in self.st_list:
            ori_height += self.fun_计算单行实际高度(comb)
        return ori_height

    def fun_计算单行实际高度(self, com_list: ComList):
        pic_width = self.st_width - ((len(com_list.img_list) + 1) * self.gutter)
        return pic_width / com_list.ratio

    @cached_property
    def fun_计算整体缩小比例(self):
        ori_height = self.st_height - ((len(self.st_list) + 1) * self.gutter)
        return self.fun_计算原始高度 / ori_height

    def fun_全自适应单行(self, com_list: ComList, num: int):
        """宽度和高度全部自适应"""
        single_ling_actual_width = int(self.st_width - ((len(com_list.img_list) + 1) * self.gutter))

        if num % 2 == 0:
            single_ling_actual_height = int((single_ling_actual_width / com_list.ratio) / self.fun_计算整体缩小比例) + 1
        else:
            single_ling_actual_height = int((single_ling_actual_width / com_list.ratio) / self.fun_计算整体缩小比例)

        bg = Image.new('RGBA', (self.st_width, single_ling_actual_height), self.bg_color)
        left = self.gutter
        img_list = list(com_list.img_list)
        random.shuffle(img_list)

        for num, img_path in enumerate(img_list):
            with Image.open(img_path.img_path).convert('RGBA') as im:
                small_im_width = int(single_ling_actual_width * (img_path.ratio / com_list.ratio))
                small_im = self.fun_制作小图片(im, small_im_width, single_ling_actual_height, num)
                bg.paste(small_im, (left, 0), small_im)
                left += small_im.width + self.gutter
                small_im.close()
        return bg

    def fun_等分单行(self, com_list: ComList):
        """图片的宽高全部一致"""
        single_line_actual_width = int(self.st_width - ((len(com_list.img_list) + 1) * self.gutter))
        single_ling_actual_height = int((self.st_height - ((self.st_row + 1) * self.gutter)) / self.st_row)
        small_im_width = int(single_line_actual_width / len(com_list.img_list))

        bg = Image.new('RGBA', (self.st_width, single_ling_actual_height), self.bg_color)
        left = self.gutter
        for num, img_path in enumerate(com_list.img_list):
            with Image.open(img_path.img_path).convert('RGBA') as im:
                small_im = self.fun_制作小图片(im, small_im_width, single_ling_actual_height, 1)
                bg.paste(small_im, (left, 0), small_im)
                left += small_im.width + self.gutter
                small_im.close()

        return bg

    def main(self):
        bg = Image.new('RGBA', (self.st_width, self.st_height), self.bg_color)
        left, top = 0, self.gutter
        for num, com_list in enumerate(self.st_list):
            line_pil = None
            if self.small_pic_size_mode == SmallSizeModel.AUTO:
                line_pil = self.fun_自适应单行(com_list)
            elif self.small_pic_size_mode == SmallSizeModel.ALL_AUTO:
                line_pil = self.fun_全自适应单行(com_list, num)
            elif self.small_pic_size_mode == SmallSizeModel.AVERAGE:
                line_pil = self.fun_等分单行(com_list)

            bg.paste(line_pil, (left, top), line_pil)
            top += line_pil.height + self.gutter
            line_pil.close()

        return bg
