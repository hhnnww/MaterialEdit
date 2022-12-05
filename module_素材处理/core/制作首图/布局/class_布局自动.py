from itertools import combinations
from typing import List

from PIL import Image

from module_素材处理.core.制作首图.布局.class_type import MyImg, ComList

Image.MAX_IMAGE_PIXELS = None


class STAutoLayout:
    """
    传入一个图片列表
    进行首图的图片排列
    """

    def __init__(self, img_list: List[str], st_width: int, st_height: int, st_row: int):
        self.img_list = img_list
        self.pil_list = self.fun_构建图片列表()
        self.st_width = st_width
        self.st_height = st_height
        self.st_row = st_row
        self.single_line_scale = self.st_width / (self.st_height / self.st_row)
        self.single_pic_num = 7

    def fun_构建图片列表(self) -> List[MyImg]:
        pil_list = []
        for img_path in self.img_list:
            with Image.open(img_path) as im:
                my_img = MyImg(
                    img_path=img_path,
                    ratio=im.width / im.height
                )
            pil_list.append(my_img)
        return pil_list

    @staticmethod
    def fun_构建单个COMB组合(in_list: List[MyImg], abs_ratio: float) -> ComList:
        all_ratio = sum([my_img.ratio for my_img in in_list])
        comb_obj = ComList(
            img_list=in_list,
            ratio=all_ratio,
            diff_ratio=abs(all_ratio - abs_ratio)
        )
        return comb_obj

    def fun_构建所有COMB组合(self) -> List[ComList]:
        all_comb = []

        for x in range(1, self.single_pic_num):
            for comb in combinations(self.pil_list, x):
                all_comb.append(self.fun_构建单个COMB组合(comb, self.single_line_scale))

        all_comb.sort(key=lambda k: k.diff_ratio)

        return all_comb

    @staticmethod
    def fun_判断是否在首图组合(com_list: ComList, st_list: List[ComList]) -> bool:
        for single_my_img in com_list.img_list:

            for line_list in st_list:
                if single_my_img in line_list.img_list:
                    return True

        return False

    def main(self) -> List[ComList]:
        st_list = []
        all_comb_list = self.fun_构建所有COMB组合()

        for in_com_list in all_comb_list:
            if self.fun_判断是否在首图组合(in_com_list, st_list) is False:
                st_list.append(in_com_list)

            if len(st_list) == self.st_row:
                break

        return st_list
