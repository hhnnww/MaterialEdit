from pathlib import Path
from typing import Optional

from module_素材处理.core.setting import IMAGE_FILE_SUFFIX
from module_素材处理.core.setting import MATERIAL_FILE_SUFFIX


class MaterialFolderRename:
    def __init__(self, folder: Path, tb_name: str):
        self.folder = folder
        self.tb_name = tb_name

        self.main()

    @staticmethod
    def is_material_file(in_file: Path) -> bool:
        if in_file.is_file() and in_file.suffix.lower() in MATERIAL_FILE_SUFFIX:
            return True

        return False

    @staticmethod
    def get_image_file(in_file: Path) -> Optional[Path]:
        for image_suffix in IMAGE_FILE_SUFFIX:
            img_path = in_file.with_suffix(image_suffix)
            if img_path.exists() is True:
                return img_path

        return None

    def fun_修改单个文件(self, in_file: Path, num: int):
        if self.is_material_file(in_file):
            img_file = self.get_image_file(in_file)

            # 判断新图片文件是否存在
            if img_file is not None:
                new_img_file = img_file.with_stem(self.tb_name + f'({num})')
                while new_img_file.exists() is True:
                    num += 1
                    new_img_file = img_file.with_stem(self.tb_name + f'({num})')

            # 判断素材文件是否存在
            new_ma_file = in_file.with_stem(self.tb_name + f'({num})')
            while new_ma_file.exists() is True:
                num += 1
                new_ma_file = in_file.with_stem(self.tb_name + f'({num})')

            # 修改源文件名字
            print(f'文件重命名：{in_file.as_posix().encode("utf-8")}')
            in_file.rename(in_file.with_stem(self.tb_name + f'({num})'))

            # 修改图片名字
            if img_file is not None:
                print(f'文件重命名：{img_file}')
                img_file.rename(img_file.with_stem(self.tb_name + f'({num})'))

            num += 1

        return num

    def all_file(self):
        all_file = []
        for in_file in self.folder.rglob('*'):
            if in_file.is_file():
                all_file.append(in_file)

        all_file.sort(key=lambda k: k.suffix.lower())
        return all_file

    def main(self):
        num = 1
        for in_file in self.all_file():
            num = self.fun_修改单个文件(in_file, num)
