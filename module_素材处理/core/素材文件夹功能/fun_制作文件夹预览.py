from pathlib import Path
from typing import List

from PIL import Image
from tqdm import tqdm

from module_素材处理.core.setting import IMAGE_FILE_SUFFIX
from module_素材处理.core.setting import MATERIAL_FILE_SUFFIX
from module_素材处理.core.图片编辑 import PICEdit
from module_素材处理.core.素材文件夹功能.fun_指定遍历 import fun_指定遍历


class MakePathPreviewImage:
    def __init__(self, in_path: Path):
        self.in_path = in_path

        self.pic_width = 2500
        self.gutter = 20
        self.info_height = 150
        self.line_pic_num = 5

    def fun_构建文件夹(self):
        path_list = []
        for in_folder in self.in_path.iterdir():
            if in_folder.is_dir():
                path_list.append(in_folder)

        return path_list

    @staticmethod
    def fun_文件夹获取所有图片(in_folder: Path) -> List[Path]:
        img_list = fun_指定遍历(folder=in_folder, suffix=IMAGE_FILE_SUFFIX)
        return img_list

    def fun_构建图片列表(self, img_list) -> List[List[Path]]:
        new_list = []
        in_list = []
        for num, img in enumerate(img_list):
            in_list.append(img)

            if len(in_list) == self.line_pic_num:
                new_list.append(in_list.copy())
                in_list = []

            if num + 1 == len(img_list) and len(in_list) > 0:
                new_list.append(in_list.copy())
                in_list = []

        return new_list

    @staticmethod
    def fun_查找对应源文件(img_path: Path):
        for suffix in MATERIAL_FILE_SUFFIX:
            ma_path = img_path.with_suffix(suffix)
            if ma_path.exists() is True:
                return ma_path

        return False

    def fun_构建单行(self, img_list: List[Path]) -> Image.Image:
        pil_list = []
        for img in img_list:
            pil = Image.open(img.as_posix())
            ma_obj = self.fun_查找对应源文件(img)
            if ma_obj is not False:
                pil.ma_name = ma_obj.name

            pil_list.append(pil)

        line_all_radio = sum([pil.width / pil.height for pil in pil_list])

        ori_width = self.pic_width - ((len(pil_list)+1) * self.gutter)
        pic_height = int((ori_width / line_all_radio)) + self.info_height

        bg = Image.new('RGBA', (self.pic_width, pic_height), (255, 255, 255))

        left = self.gutter
        top = self.gutter
        for pil in pil_list:
            pil_width = int(ori_width / (line_all_radio / (pil.width / pil.height)))
            if pil_width > self.pic_width / 5:
                pil_width = int(self.pic_width / 5)

            pil.thumbnail((pil_width, 9999), 1)
            pil = self.fun_单个图片加名字(pil)
            bg.paste(pil, (left, top), pil)
            left += pil.width + self.gutter
            pil.close()

        return bg

    def fun_单个图片加名字(self, pil: Image.Image):
        ma_name = str(pil.ma_name).upper()
        bg = Image.new('RGBA', (pil.width, pil.height + self.info_height), (255, 255, 255))
        pil = PICEdit.fun_图片圆角(pil, 20).main()
        bg.paste(pil, (0, 0), pil)
        pil.close()

        gutter = 10
        ma_name = PICEdit.fun_单行文字(text=ma_name, font_weight='r', font_size=220, text_color=(120, 120, 120),
                                       bg_color=(255, 255, 255)).main()
        ma_name.thumbnail((bg.width - (gutter * 10), 9999), 1)
        bg.paste(ma_name, (0, pil.height + (gutter * 2)), ma_name)
        ma_name.close()
        return bg

    def fun_文件夹构建整体(self, in_folder: Path):
        img_list = self.fun_文件夹获取所有图片(in_folder)
        img_list = self.fun_构建图片列表(img_list)
        pil_list = [self.fun_构建单行(pil) for pil in img_list]
        height = sum([pil.height for pil in pil_list])
        bg = Image.new('RGBA', (self.pic_width, height), (255, 255, 255))
        top = 0
        for pil in pil_list:
            bg.paste(pil, (0, top), pil)
            top += pil.height
            pil.close()

        png_path = in_folder.parent / (in_folder.stem + '.png')
        bg.save(png_path)
        bg.close()

    def main(self):
        for in_folder in tqdm(self.fun_构建文件夹(), desc='构建文件夹预览图', ncols=100):
            print(f'\n制作预览图:{in_folder}\n')
            self.fun_文件夹构建整体(in_folder)


if __name__ == '__main__':
    path_img = MakePathPreviewImage(
        in_path=Path(r'F:\泡泡素材\10000-19999\10001\10001')
    )
    path_img.main()
