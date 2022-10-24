import shutil
from functools import cached_property
from pathlib import Path


class MaterialFolderStructure:
    def __init__(self, root_path: str):
        self.root_path = self.fun_检查ROOT_PATH(root_path)
        self.move_file()

    @staticmethod
    def fun_检查ROOT_PATH(root_path: str):
        root_path = Path(root_path)

        if root_path.exists() is False:
            raise IndexError('文件夹不存在')

        if len(root_path.parts) < 3:
            raise IndexError('路径太短')

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


if __name__ == '__main__':
    mp = MaterialFolderStructure(r'E:\DOWN\cute-cat-logo-mascot')
    print(mp.root_path)
