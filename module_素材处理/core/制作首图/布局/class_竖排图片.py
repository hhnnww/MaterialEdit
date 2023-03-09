from dataclasses import dataclass
from typing import List
from functools import cached_property
from PIL import Image

from module_素材处理.core.制作首图.布局.class_type import MyImg
from module_素材处理.core.图片编辑.class_picedit import PICEdit

Image.MAX_IMAGE_PIXELS = None


@dataclass
class LayoutProportion:
    coly: int
    ratio: float
    diff: float


class VerticalImages:
    def __init__(self, pic_list: List[str], st_width: int, st_height: int, gutter: int):
        self.pic_list = pic_list
        self.pil_list = self.fun_构建列表()

        self.st_width = st_width
        self.st_height = st_height
        self.gutter = gutter

    def fun_构建列表(self) -> List[MyImg]:
        my_img_list = []
        for pic in self.pic_list:
            with Image.open(pic) as im:
                my_img_list.append(
                    MyImg(
                        img_path=pic,
                        ratio=im.width / im.height
                    )
                )

        return my_img_list

    def fun_计算所有平均比例(self):
        return sum([img.ratio for img in self.pil_list]) / len(self.pil_list)

    def fun_计算不同布局的各种比例(self):
        ratio_list = []
        for x in range(2, 6):
            first_pic_ratio = ((self.st_width / (x + 1)) * 2) / self.st_height
            ratio_list.append(
                LayoutProportion(coly=x, ratio=first_pic_ratio, diff=0)
            )
        return ratio_list

    @cached_property
    def fun_计算最合适的比例(self):
        all_layout_ratio = self.fun_计算不同布局的各种比例()
        average_proportion = self.fun_计算所有平均比例()
        for comb_img in all_layout_ratio:
            comb_img.diff = abs(comb_img.ratio - average_proportion)
        all_layout_ratio.sort(key=lambda k: k.diff)
        return all_layout_ratio[0]

    def fun_制作第一张图(self, img: MyImg):
        best_comb = self.fun_计算最合适的比例
        ori_width = self.st_width - ((best_comb.coly + 1) * self.gutter)
        width = int((ori_width / (self.fun_计算最合适的比例.coly + 1)) * 2)
        height = self.st_height - (self.gutter * 2)

        pil = PICEdit.fun_图片裁剪(im=Image.open(img.img_path), width=width, height=height)
        if self.gutter > 0:
            pil = PICEdit.fun_图片圆角(img=pil, radius=20).main()

        if pil.mode != 'RGBA':
            pil = pil.convert('RGBA')

        return pil

    def fun_制作后面的小图(self, img: MyImg):
        best_comb = self.fun_计算最合适的比例
        ori_width = self.st_width - ((best_comb.coly + 1) * self.gutter)
        ori_height = self.st_height - (self.gutter * 3)

        width = int(ori_width / (best_comb.coly + 1))
        height = int(ori_height / 2)

        pil = PICEdit.fun_图片裁剪(im=Image.open(img.img_path), width=width, height=height)
        if self.gutter > 0:
            pil = PICEdit.fun_图片圆角(img=pil, radius=20).main()

        if pil.mode != 'RGBA':
            pil = pil.convert('RGBA')

        return pil

    def main(self):
        best_comb = self.fun_计算最合适的比例
        img_count = (best_comb.coly * 2) - 1
        self.pil_list = self.pil_list[:img_count + 1]

        bg = Image.new('RGBA', (self.st_width, self.st_height), (255, 255, 255))
        first_pic = self.fun_制作第一张图(self.pil_list[0])
        bg.paste(first_pic, (self.gutter, self.gutter), first_pic)

        coordinate_x = self.gutter + first_pic.width + self.gutter
        coordinate_y = self.gutter

        for img in self.pil_list[1:]:
            pil = self.fun_制作后面的小图(img)
            bg.paste(pil, (coordinate_x, coordinate_y), pil)
            coordinate_x += pil.width + self.gutter

            if coordinate_x >= self.st_width:
                coordinate_x = self.gutter + first_pic.width + self.gutter
                coordinate_y = (self.gutter * 2) + pil.height

            pil.close()

        first_pic.close()
        return bg


if __name__ == '__main__':
    from pathlib import Path

    pic_list = []
    for in_file in Path(r'E:\小夕素材\9000-9999\9286\9286\000_099').iterdir():
        if in_file.is_file() and in_file.suffix.lower() in ['.png']:
            pic_list.append(in_file.as_posix())

    vi = VerticalImages(
        pic_list=pic_list,
        st_width=1500,
        st_height=1300,
        gutter=16
    )

    vi.main().show()
