from itertools import combinations
from typing import List

from PIL import Image

from module_素材处理.core.制作首图.布局.class_type import MyImg, ComList

Image.MAX_IMAGE_PIXELS = None


class STLayoutOneX:
    """
    传入一个扸列表
    第一个图片作为大图
    剩下的自由排列，找到最适合的作为第二行
    """

    def __init__(self, pic_list: List[str], st_width: int, st_height: int):
        self.pic_list = pic_list
        self.pil_list = self.fun_构建列表()

        self.st_width = st_width
        self.st_height = st_height

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

    @staticmethod
    def fun_构建comb(in_list: List[MyImg], abs_ratio: float) -> ComList:
        all_ratio = sum([my_img.ratio for my_img in in_list])
        return ComList(
            img_list=in_list,
            ratio=all_ratio,
            diff_ratio=abs(all_ratio - abs_ratio)
        )

    def fun_计算第二行比例(self) -> float:
        first_line_height = self.st_width / self.pil_list[0].ratio
        last_line_height = self.st_height - first_line_height
        last_line_ratio = self.st_width / last_line_height

        return last_line_ratio

    def main(self) -> List[ComList]:
        comb_one = self.fun_构建comb([self.pil_list[0]], 0)
        if len(self.pil_list) == 1:
            return [comb_one]

        second_row_ratio = self.fun_计算第二行比例()

        self.pil_list = self.pil_list[1:]
        last_line_comb_list = []
        for x in range(1, 5):
            for comb in combinations(self.pil_list, x):
                last_line_comb_list.append(self.fun_构建comb(comb, second_row_ratio))

        last_line_comb_list.sort(key=lambda k: k.diff_ratio)

        st_list = [
            comb_one, last_line_comb_list[0]
        ]

        return st_list
