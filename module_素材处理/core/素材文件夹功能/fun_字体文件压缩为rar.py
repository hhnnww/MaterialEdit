import subprocess
from pathlib import Path
from tqdm import tqdm
from module_素材处理.core.素材文件夹功能.fun_指定遍历 import fun_指定遍历


def fun_字体文件压缩为rar(in_path: Path) -> None:
    all_file = fun_指定遍历(folder=in_path, suffix=['.otf', '.ttf'])
    rar_exe = r'C:\Program Files\WinRAR\WinRAR.exe'
    for font_path in tqdm(all_file, desc='压缩字体文件为rar', ncols=100):
        rar_path = font_path.with_suffix('.rar')
        args = f'{rar_exe} a {rar_path.as_posix()} {font_path.name}'
        cwd_path = font_path.parent.as_posix()

        subprocess.check_output(
            args=args, cwd=cwd_path
        )

        print('\n')
        print(font_path.name)
        print('\n')

        font_path.unlink()


if __name__ == '__main__':
    fun_字体文件压缩为rar(
        Path(r'E:\小夕素材\9000-9999\9261\9261')
    )

    # subprocess.run(
    #     r'C:\Program Files\WinRAR\WinRAR.exe a E:\小夕素材\9000-9999\9261\9261\000_099\小夕素材(1).rar 小夕素材(1).otf',
    #     cwd=r'E:\小夕素材\9000-9999\9261\9261\000_099')
