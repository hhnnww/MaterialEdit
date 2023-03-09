from typing import List

from PIL import Image

from module_素材处理.core.制作首图.布局.class_type import MyImg
from module_素材处理.core.图片编辑.class_picedit import PICEdit

Image.MAX_IMAGE_PIXELS = None


class HorizontalImage:
    def __init__(self, pic_list: List[str], st_width: int, st_height: int, gutter: int):
        self.pic_list = pic_list
        self.pil_list = self.fun_构建列表()[:10]

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

    def fun_制作第一张图片(self, img: MyImg):
        im = Image.open(img.img_path).convert('RGBA')
        width = int(((self.st_width - (self.gutter * 3)) / 3) * 2) + 3
        height = int(((self.st_height - (self.gutter * 5)) / 4) * 2) + self.gutter

        im = PICEdit.fun_图片裁剪(im, width=width, height=height)
        if self.gutter > 0:
            im = PICEdit.fun_图片圆角(img=im, radius=20).main()

        return im

    def fun_制作小图(self, img: MyImg):
        im = Image.open(img.img_path).convert('RGBA')
        width = int((self.st_width - (self.gutter * 4)) / 3)
        height = int((self.st_height - (self.gutter * 5)) / 4)

        im = PICEdit.fun_图片裁剪(im, width=width, height=height)
        if self.gutter > 0:
            im = PICEdit.fun_图片圆角(img=im, radius=20).main()

        return im

    def main(self):
        bg = Image.new('RGBA', (self.st_width, self.st_height), (255, 255, 255))
        colx, coly = self.gutter, self.gutter
        for num, img in enumerate(self.pil_list):
            if num == 0:
                im = self.fun_制作第一张图片(img)
                bg.paste(im, (colx, coly), im)
                colx += im.width + self.gutter
            else:
                im = self.fun_制作小图(img)

                if num < 3:
                    im = self.fun_制作小图(img)
                    bg.paste(im, (colx, coly), im)
                    coly += im.height + self.gutter

                elif num >= 3:
                    if num == 3:
                        colx = self.gutter

                    im = self.fun_制作小图(img)
                    bg.paste(im, (colx, coly), im)
                    colx = im.width + self.gutter + colx

                    if num == 5:
                        coly += im.height + self.gutter
                        colx = self.gutter

            im.close()

        return bg


if __name__ == '__main__':
    from pathlib import Path

    pic_list = []
    for in_file in Path(r'E:\小夕素材\9000-9999\9287\9287').iterdir():
        if in_file.is_file() and in_file.suffix.lower() in ['.png']:
            pic_list.append(in_file.as_posix())

    hi = HorizontalImage(pic_list=pic_list, st_width=1500, st_height=1300, gutter=16)
    hi.main().show()
