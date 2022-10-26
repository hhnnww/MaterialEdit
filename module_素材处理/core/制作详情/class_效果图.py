from functools import cached_property
from pathlib import Path
from typing import List

from PIL import Image

from module_素材处理.core.setting import PIC_EDIT_IMG
from module_素材处理.core.图片编辑.class_picedit import PICEdit


class XQEffectPIC:
    def __init__(self, img_list: List[Path], tb_name: str):
        self.img_list = img_list
        self.tb_name = tb_name

        self.gutter = 30
        self.bg_width = 1500

    @cached_property
    def fun_单排图片实际宽度(self):
        pic_actual = int(self.bg_width - (self.gutter * 2))
        return pic_actual

    @cached_property
    def fun_计算整体高度(self):
        height = self.gutter
        for img in self.img_list:
            with Image.open(img.as_posix()) as im:
                small_im_height = int(self.fun_单排图片实际宽度 / (im.width / im.height))
                height += small_im_height + self.gutter

        return height

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

    def fun_制作小图(self, img):
        im = Image.open(img.as_posix()).convert('RGBA')
        height = int(self.fun_单排图片实际宽度 / (im.width / im.height))
        im = im.resize((self.fun_单排图片实际宽度, height), 1)
        im = PICEdit.fun_图片圆角(im, 20).main()
        return im

    def main(self):
        bg = Image.new('RGBA', (self.bg_width, self.fun_计算整体高度), (255, 255, 255))
        top = self.gutter
        for num, img in enumerate(self.img_list):
            small_im = self.fun_制作小图(img)
            if num % 2 != 0:
                small_im = self.fun_单个图片添加水印(small_im)

            bg.paste(small_im, (self.gutter, top), small_im)
            top += small_im.height + self.gutter
            small_im.close()

        return bg


if __name__ == '__main__':
    from core.素材文件夹功能.fun_指定遍历 import fun_指定遍历
    from pathlib import Path

    il = [p.as_posix() for p in fun_指定遍历(Path(r'G:\饭桶设计\0-999\0055\效果图'), ['.png'])]
    xgt = XQEffectPIC(
        img_list=fun_指定遍历(Path(r'G:\饭桶设计\1000-1999\1023\效果图'), ['.png'])
    ).main()
    xgt.show()
