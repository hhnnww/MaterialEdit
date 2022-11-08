import re
import shutil
from functools import cached_property
from pathlib import Path
from random import shuffle

from pydantic import BaseModel

from module_素材处理.core.setting import IMAGE_FILE_SUFFIX
from module_素材处理.core.素材文件夹功能.fun_指定遍历 import fun_指定遍历


class PathType(BaseModel):
    exist: bool = True
    stem: str = ''
    path: str = ''


class ImageType(BaseModel):
    path: str = ''
    name: str = ''


class MaterialFolderStructure:
    def __init__(self, root_path: str):
        self.root_path = self.fun_检查ROOT_PATH(root_path)
        self.move_file()

    @staticmethod
    def fun_检查ROOT_PATH(root_path: str):
        root_path = Path(root_path)

        if root_path.exists() is False:
            root_path.mkdir()

        if len(root_path.parts) < 3:
            raise IndexError('路径太短')

        if '-' in root_path.stem:
            raise IndexError('可能是分类文件夹')

        if root_path.parent.stem == root_path.stem:
            raise IndexError('父子STEM相同')

        if root_path.is_absolute() is False:
            raise IndexError('是相对路径')

        return root_path

    @cached_property
    def material_path(self):
        return self.root_path / self.root_path.stem

    @cached_property
    def effect_path(self):
        return self.root_path / '效果图'

    @cached_property
    def preview_path(self):
        return self.root_path / '预览图'

    def move_file(self):

        # 创建素材文件夹
        if self.material_path.exists() is False:
            self.material_path.mkdir()

        for in_file in self.root_path.iterdir():
            # 文件移动到素材文件夹
            if in_file.is_file():
                file_new_name = self.material_path / in_file.name
                num = 1
                while file_new_name.exists() is True:
                    file_new_name = self.material_path / f'{in_file.stem}({num}){in_file.suffix}'
                    num += 1

                shutil.move(in_file, file_new_name)

            # 文件夹移动到素材文件夹
            if in_file.is_dir() and in_file not in [self.material_path, self.effect_path, self.preview_path]:
                dir_new_name = self.material_path / in_file.name
                num = 1
                while dir_new_name.exists() is True:
                    file_new_name = self.material_path / f'{in_file.stem}({num}){in_file.suffix}'
                    num += 1
                in_file.rename(dir_new_name)

    @cached_property
    def fun_获取素材文件夹ID(self):
        num = re.findall('\d+', self.root_path.stem)
        if len(num) > 0:
            num_int = int(num[0])
            return num_int

        return None

    @cached_property
    def prev_path(self):
        obj = PathType(exist=True, path='')

        if self.fun_获取素材文件夹ID is None:
            obj.exist = False

        if self.fun_获取素材文件夹ID <= 0:
            obj.exist = False

        prev_num_int = self.fun_获取素材文件夹ID - 1
        prev_num_text = str(prev_num_int)
        while len(prev_num_text) < len(self.root_path.stem):
            prev_num_text = '0' + prev_num_text

        prev_path = self.root_path.parent / prev_num_text
        obj.path = prev_path.as_posix()
        obj.stem = prev_path.stem

        return obj.dict()

    @cached_property
    def next_path(self):
        obj = PathType()

        if self.fun_获取素材文件夹ID is None:
            obj.exist = False

        prev_num_int = self.fun_获取素材文件夹ID + 1
        prev_num_text = str(prev_num_int)
        while len(prev_num_text) < len(self.root_path.stem):
            prev_num_text = '0' + prev_num_text

        prev_path = self.root_path.parent / prev_num_text
        obj.path = prev_path.as_posix()
        obj.stem = prev_path.stem

        return obj.dict()

    @cached_property
    def effect_img_list(self):
        if self.effect_path.exists() is False:
            return []

        img_list = []
        for in_file in fun_指定遍历(self.effect_path, IMAGE_FILE_SUFFIX):
            img_obj = ImageType()
            img_obj.path = in_file.as_posix()
            img_obj.name = in_file.name

            img_list.append(img_obj.dict())

        return img_list

    @cached_property
    def preview_img_list(self):
        if self.preview_path.exists() is False:
            return []

        img_list = []
        for in_file in fun_指定遍历(self.preview_path, IMAGE_FILE_SUFFIX):
            img_obj = ImageType()
            img_obj.path = in_file.as_posix()
            img_obj.name = in_file.name

            img_list.append(img_obj.dict())

        return img_list


if __name__ == '__main__':
    mp = MaterialFolderStructure(r'G:\饭桶设计\0-999\0055')
    print(mp.prev_path)
    print(mp.next_path)
