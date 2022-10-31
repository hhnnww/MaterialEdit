from dataclasses import dataclass
from functools import cached_property
from typing import List, Tuple

from PIL import Image

from module_素材处理.core.图片编辑.fun_图片圆角 import PICToCircle


@dataclass
class ImageType:
    path: str
    width: int
    height: int
    ratio: float


class STLayoutScat:
    def __init__(self, img_list: List[str], gutter: int, st_row: int, st_width: int, st_height: int):
        self.img_list = img_list
        self.gutter = gutter
        self.st_row = st_row
        self.st_width = st_width
        self.st_height = st_height

    @cached_property
    def pil_list(self) -> List[ImageType]:
        pil_list = []
        for in_file in self.img_list:
            with Image.open(in_file) as im:
                pil_list.append(
                    ImageType(path=in_file, width=im.width, height=im.height, ratio=im.width / im.height)
                )

        return pil_list

    @cached_property
    def fun_单行高度(self) -> int:
        return int((self.st_height - ((self.st_row + 1) * self.gutter)) / self.st_row)

    def fun_计算单行COMB的宽度(self, single_comb: List[ImageType]) -> int:
        single_all_ratio = sum([img.ratio for img in single_comb])
        single_width = int((self.fun_单行高度 * single_all_ratio) + (len(single_comb) + 1) * self.gutter)
        return single_width

    @cached_property
    def fun_首图组合(self) -> List[List[ImageType]]:
        st_comb, single_comb = [], []

        for in_image_type in self.pil_list:
            single_comb.append(in_image_type)

            if self.fun_计算单行COMB的宽度(single_comb) > self.st_width:
                st_comb.append(single_comb.copy())
                single_comb = []

        return st_comb

    def fun_制作单行(self, single_comb: List[ImageType]) -> Tuple[Image.Image, int]:
        first_width = 0

        line_pil_width = self.fun_计算单行COMB的宽度(single_comb)
        line_pil_height = self.fun_单行高度

        bg = Image.new('RGBA', (line_pil_width, line_pil_height), (255, 255, 255))
        left, top = self.gutter, 0
        for num, in_image_type in enumerate(single_comb):
            im = Image.open(in_image_type.path).convert('RGBA')
            im = im.resize((int(line_pil_height * in_image_type.ratio), line_pil_height), resample=1)
            if self.gutter > 0:
                im = PICToCircle(im, 20).main()

            bg.paste(im, (left, top), im)
            left += im.width + self.gutter

            if num == 0:
                first_width = int(im.width / 2)

            im.close()

        return bg, first_width

    def main(self):
        bg = Image.new('RGBA', (self.st_width, self.st_height), (255, 255, 255))
        top = self.gutter
        for num, single_comb in enumerate(self.fun_首图组合):
            single_pil = self.fun_制作单行(single_comb)

            if num % 2 != 0:
                single_crop_pil = single_pil[0].crop(
                    (
                        0,
                        0,
                        self.st_width,
                        single_pil[0].height
                    )
                )
            else:

                left = single_pil[1]
                if left > single_pil[0].width - self.st_width:
                    left = int((single_pil[0].width - self.st_width) / 2)

                single_crop_pil = single_pil[0].crop(
                    (
                        left, 0,
                        left + self.st_width,
                        single_pil[0].height
                    )
                )

            bg.paste(single_crop_pil, (0, top), single_crop_pil)
            top += single_crop_pil.height + self.gutter
            single_crop_pil.close()

        return bg


if __name__ == '__main__':
    from pathlib import Path

    all_file = []
    for in_file in Path(r'G:\饭桶设计\1000-1999\1808\预览图').iterdir():
        if in_file.is_file() and in_file.suffix.lower() in ['.png']:
            all_file.append(in_file.as_posix())

    STLayoutScat(all_file, 10, 3, 1500, 1300).main().show()
