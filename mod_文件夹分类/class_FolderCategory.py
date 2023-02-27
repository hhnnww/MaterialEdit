import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator
from typing import List

from module_素材处理.core.setting import IMAGE_FILE_SUFFIX
from module_素材处理.core.setting import MATERIAL_FILE_SUFFIX


@dataclass
class MaterialOBJ:
    material_path: str
    preview_path: str
    image_path: str


@dataclass
class FolderOBJ:
    folder_path: str
    folder_stem: str
    preview_path: str


class FolderCategory:
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.preview_path = self.root_path / '预览图'
        self.material_path = self.root_path / self.root_path.stem

    @staticmethod
    def get_stem_num(stem: str):
        """
        获取stem的数字,用来给文件列表排序
        :param stem:
        :return:
        """
        num = re.findall('\d+', stem)
        num = ''.join(num)
        if len(num) > 0:
            return int(num)

        return 0

    def all_material_file(self):
        """
        获取所有源文件列表
        :return:
        """
        f = []
        for in_file in self.material_path.iterdir():
            if in_file.is_file() and in_file.suffix.lower() in MATERIAL_FILE_SUFFIX:
                f.append(in_file)

        f.sort(key=lambda k: self.get_stem_num(k.stem))

        return f

    def make_material_obj(self, material_file_path: Path):
        """
        源文件构建成一个obj
        对应预览图,素材预览图
        :param material_file_path:
        :return:
        """
        ma_obj = MaterialOBJ(
            material_path='',
            image_path='',
            preview_path=''
        )
        ma_obj.material_path = material_file_path.as_posix()
        for suffix in IMAGE_FILE_SUFFIX:
            img_path = material_file_path.with_suffix(suffix)
            if img_path.exists() is True:
                ma_obj.image_path = img_path.as_posix()
                ma_obj.preview_path = self.get_preview_path(img_path)
        return ma_obj

    def get_preview_path(self, img_path: Path):
        """
        找到素材图对应的预览图
        :param img_path:
        :return:
        """
        if self.preview_path.exists() is False:
            return None

        material_len = len(self.material_path.parts)
        img_parts = list(img_path.parts)
        img_parts[:material_len] = list(self.preview_path.parts)
        prev_path = Path('/'.join(img_parts))
        print(prev_path)
        if prev_path.exists() is True:
            return prev_path.as_posix()

        return None

    def all_material_obj(self) -> Iterator[MaterialOBJ]:
        """
        获取所有素材以及素材图预览图的模型
        :return:
        """
        for in_file in self.all_material_file():
            yield self.make_material_obj(material_file_path=in_file)

    def all_folder(self) -> Iterator[FolderOBJ]:
        """
        获取所有文件夹列表
        :return:
        """
        for in_file in self.material_path.iterdir():
            if in_file.is_dir():
                preview_path = self.preview_path / in_file.stem
                yield FolderOBJ(
                    folder_path=in_file.as_posix(),
                    folder_stem=in_file.stem,
                    preview_path=preview_path.as_posix()
                )

    def new_folder(self, stem: str):
        """
        新建一个文件夹
        :param stem:
        :return:
        """
        new_folder = self.material_path / stem
        if new_folder.exists() is False:
            new_folder.mkdir()

        preview_folder = self.preview_path / stem
        if preview_folder.exists() is False:
            preview_folder.mkdir()

    def move_material_to_folder(self, material_list: List[MaterialOBJ], folder_path: str, preview_path: str):
        """
        移动素材列表
        :param material_list:
        :param folder_path:
        :param preview_path:
        :return:
        """
        for ma_obj in material_list:
            self.move_single_material_to_folder(ma_obj=ma_obj, folder_path=folder_path, preview_path=preview_path)

    @staticmethod
    def move_single_material_to_folder(ma_obj: MaterialOBJ, folder_path: str, preview_path: str):
        """
        移动单个素材
        :param ma_obj:
        :param folder_path:
        :param preview_path:
        :return:
        """
        folder_path = Path(folder_path)
        preview_path = Path(preview_path)

        # 移动素材
        material_file = Path(ma_obj.material_path)
        new_material_file = folder_path / material_file.name
        material_file.rename(new_material_file)

        # 移动素材图
        img_file = Path(ma_obj.image_path)
        img_file.rename(folder_path / img_file.name)

        # 移动预览图
        preview_file = Path(ma_obj.preview_path)
        preview_file.rename(preview_path / preview_file.name)


if __name__ == '__main__':
    fc = FolderCategory(
        root_path=r'F:\泡泡素材\10000-19999\10001'
    )

    fc.new_folder('柜子')
