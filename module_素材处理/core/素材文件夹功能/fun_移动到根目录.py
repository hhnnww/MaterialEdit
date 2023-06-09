import shutil
from pathlib import Path


def fun_移动到根目录(folder: Path):
    for in_file in folder.rglob('*'):
        if in_file.is_file():
            if in_file.parent != folder:
                new_path = folder / in_file.name

                num = 1
                while new_path.exists() is True:
                    new_path = folder / (in_file.stem + f' ({num})' + in_file.suffix)
                    num += 1

                print(f'移动到根目录:{new_path.as_posix().encode("utf-8")}')
                in_file.rename(new_path)

    # 删除所有文件夹
    for in_file in folder.iterdir():
        if in_file.is_dir():
            print(f'删除多余文件夹：{in_file}')
            shutil.rmtree(in_file)
