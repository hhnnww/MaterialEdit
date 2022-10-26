import shutil
from pathlib import Path

from module_素材处理.core.setting import IMAGE_FILE_SUFFIX
from module_素材处理.core.素材文件夹功能.fun_指定遍历 import fun_指定遍历


def fun_复制图片到指定目录(ori: Path, dst: Path, rename: bool = False):
    if dst.exists() is False:
        dst.mkdir()

    num = 1
    for in_file in fun_指定遍历(ori, IMAGE_FILE_SUFFIX):
        in_file_parts = list(in_file.parts)
        ori_parts = list(ori.parts)
        dst_parts = list(dst.parts)

        in_file_parts[:len(ori_parts)] = dst_parts
        new_file = Path('\\'.join(in_file_parts))

        if new_file.exists() is True:
            print('目标文件存在:' + new_file.as_posix())
            continue

        if rename is True:
            new_file = new_file.with_stem(f'{num}')
            num += 1

        shutil.copy(in_file, new_file)


if __name__ == '__main__':
    fun_复制图片到指定目录(
        ori=Path(r'G:\饭桶设计\0-999\0055\0055'),
        dst=Path(r'G:\饭桶设计\0-999\0055\预览图')
    )
