from pathlib import Path
from pprint import pprint
from typing import List
from typing import Optional

from module_素材处理.core.素材文件夹功能.fun_获取数字 import fun_获取数字


def fun_指定遍历(folder: Path, suffix: List[str]) -> List[Optional[Path]]:
    all_file = []
    for in_file in folder.rglob('*'):
        if in_file.is_file() and in_file.suffix.lower() in suffix:
            all_file.append(in_file)

    all_file.sort(key=lambda k: fun_获取数字(k))
    return all_file


if __name__ == '__main__':
    tf = fun_指定遍历(
        Path(r'E:\小夕素材\9000-9999\9262\预览图'), ['.png']
    )
    tf.reverse()
    pprint(tf)
