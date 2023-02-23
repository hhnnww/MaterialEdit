import subprocess
from pathlib import Path
from tqdm import tqdm
from module_素材处理.core.素材文件夹功能.fun_指定遍历 import fun_指定遍历
from typing import List


def fun_解压RAR(in_path: Path):
    all_file = fun_指定遍历(folder=in_path, suffix=['.rar'])
    rar_exe = r'C:\Program Files\WinRAR\WinRAR.exe'
    for font_path in tqdm(all_file, desc='解压RAR', ncols=100):
        font_path: Path
        print(f'\n解压RAR:{font_path.as_posix()}\n')

        args = f'{rar_exe} x {font_path.name}'
        cwd_path = font_path.parent.as_posix()

        subprocess.check_output(
            args=args, cwd=cwd_path
        )

        font_path.unlink()


if __name__ == '__main__':
    fun_解压RAR(
        in_path=Path(r'F:\泡泡素材\10000-19999\10001')
    )
