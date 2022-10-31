import shutil
from functools import cached_property
from pathlib import Path


class SCDownPathMoveMaterialPath:
    def __init__(self, tb_name: str, down_path: str, material_path: str):
        self.tb_name = tb_name
        self.down_path = Path(down_path)
        self.material_path = Path(material_path)

    @cached_property
    def fun_获取素材目录最大数字(self):
        all_dir = list(self.material_path.iterdir())
        all_dir.sort(key=lambda k: k.stem, reverse=True)
        return int(all_dir[0].stem)

    def main(self):
        num = self.fun_获取素材目录最大数字 + 1
        material_new_path = self.material_path / str(num)

        if material_new_path.exists() is True:
            raise IndexError('路径存在，无法创建')
        else:
            material_new_path.mkdir()

        for in_dir in self.down_path.iterdir():
            if in_dir.is_dir():
                print(f'移动:\t{in_dir.as_posix()}\t-->\t{material_new_path.as_posix()}')
                shutil.move(in_dir, material_new_path)

                num += 1
                material_new_path = self.material_path / str(num)


if __name__ == '__main__':
    mp = SCDownPathMoveMaterialPath(
        '饭桶设计',
        r'G:\DOWN',
        r'G:\饭桶设计\1000-1999'
    )
    print(mp.fun_获取素材目录最大数字)
