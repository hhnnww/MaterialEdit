from dataclasses import dataclass
from functools import cached_property
from typing import List

from PIL import Image

from module_素材处理.core.制作首图.布局.class_type import MyImg
from module_素材处理.core.图片编辑.class_picedit import PICEdit

Image.MAX_IMAGE_PIXELS = None


@dataclass
class LayoutProportion:
    coly: int
    ratio: float
    diff: int = 0


class HorizontalImageAuto:
    def __init__(self, pic_list: List[str], st_width: int, st_height: int, gutter: int):
        self.pic_list = pic_list
        self.pil_list = self.fun_构建列表()[:20]

        self.st_width = st_width
        self.st_height = st_height
        self.gutter = gutter

    def fun_构建列表(self) -> List[MyImg]:
        my_img_list = []
        for pic in self.pic_list:
            with Image.open(pic) as im:
                my_img_list.append(
                    MyImg(img_path=pic, ratio=im.width / im.height)
                )
        return my_img_list

    def fun_构建比例列表(self):
        all_proportion = []
        for x in range(1, 6):
            width = int(((self.st_width - (self.gutter * 3)) / 3) * 2)
            height = int((((self.st_height - (self.gutter * (x + 1))) / x) * 2) + self.gutter)
            all_proportion.append(
                LayoutProportion(
                    coly=x,
                    ratio=width / height
                )
            )

        return all_proportion

    @cached_property
    def fun_计算最合适的比例(self):
        pil_ratio = sum([img.ratio for img in self.pil_list]) / len(self.pil_list)
        all_pro = self.fun_构建比例列表()
        for pro in all_pro:
            pro.diff = abs(pro.ratio - pil_ratio)

        all_pro.sort(key=lambda k: k.diff)

        return all_pro[0]

    def fun_制作第一张图(self, img: MyImg):
        best_comb = self.fun_计算最合适的比例

        im = Image.open(img.img_path).convert('RGBA')
        width = int(((self.st_width - (self.gutter * 3)) / 3) * 2) + 3
        height = int((((self.st_height - (self.gutter * (best_comb.coly + 1))) / best_comb.coly) * 2) + self.gutter)
        im = PICEdit.fun_图片裁剪(im=im, width=width, height=height)
        if self.gutter > 0:
            im = PICEdit.fun_图片圆角(img=im, radius=20).main()

        return im

    def fun_制作小图(self, img: MyImg):
        best_comb = self.fun_计算最合适的比例

        width = int((self.st_width - (self.gutter * 4)) / 3)
        height = int((self.st_height - (self.gutter * (best_comb.coly + 1))) / best_comb.coly)
        im = Image.open(img.img_path).convert('RGBA')
        im = PICEdit.fun_图片裁剪(im, width, height)
        if self.gutter > 0:
            im = PICEdit.fun_图片圆角(im, 20).main()
        return im

    def main(self):
        bg = Image.new('RGBA', (self.st_width, self.st_height), (255, 255, 255))
        first_pic = self.fun_制作第一张图(self.pil_list[0])
        bg.paste(first_pic, (self.gutter, self.gutter), first_pic)

        colx = (self.gutter * 2) + first_pic.width
        coly = self.gutter
        y_top = 0

        first_pic.close()

        for num, img in enumerate(self.pil_list[1:]):
            im = self.fun_制作小图(img)
            bg.paste(im, (colx, coly), im)
            coly += im.height + self.gutter

            if num == 1:
                colx = self.gutter
                y_top = coly

            if coly+im.height >= self.st_height:
                coly = y_top
                colx += self.gutter + im.width

            im.close()

        return bg


if __name__ == '__main__':
    from pathlib import Path

    pic_list = []
    for in_file in Path(r'E:\小夕素材\9000-9999\9287\9287').iterdir():
        if in_file.is_file() and in_file.suffix.lower() in ['.png']:
            pic_list.append(in_file.as_posix())

    hia = HorizontalImageAuto(
        pic_list=pic_list, st_width=1500, st_height=1300, gutter=16
    )

    hia.main().show()
