import zipfile
from pathlib import Path

from module_素材处理.core.素材文件夹功能.fun_指定遍历 import fun_指定遍历


def fun_解压ZIP(in_path: Path):
    for in_file in fun_指定遍历(in_path, ['.zip']):
        if zipfile.is_zipfile(in_file.as_posix()) is False:
            print(f'损坏的zip文件：{in_file}')

        else:
            with zipfile.ZipFile(file=in_file.as_posix(), mode='r') as z_file:
                try:
                    z_file.extractall(path=(in_file.parent / in_file.stem).as_posix())
                except zipfile.BadZipfile:
                    print(f'损坏的zip文件：{in_file}')

            in_file.unlink()
