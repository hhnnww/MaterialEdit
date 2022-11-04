import shutil
from functools import cached_property
from pathlib import Path
from typing import Tuple


class UnUsedPathDir:
    def __init__(self, in_path: str):
        self.in_path = Path(in_path)

    @staticmethod
    def fun_包含文件(in_path: Path):
        for in_file in in_path.rglob('*'):
            if in_file.is_file():
                return True

        return False

    @cached_property
    def min_max_int(self) -> Tuple[int, int]:
        num_split = self.in_path.stem.split('-')
        if len(num_split) == 2:
            return int(num_split[0]), int(num_split[1])

        raise IndexError('传入的文件夹stem不正确')

    def main(self):
        for x in range(self.min_max_int[0], self.min_max_int[1] + 1):
            stem = str(x)
            while len(stem) < 4:
                stem = '0' + stem

            path_dir = self.in_path / stem

            if path_dir.exists() is True:
                if self.fun_包含文件(path_dir) is False:
                    shutil.rmtree(path_dir)

            if path_dir.exists() is False:
                yield path_dir


if __name__ == '__main__':
    from pprint import pprint

    uupd = UnUsedPathDir(r'G:\饭桶设计\0-999')
    no_path = list(uupd.main())
    pprint(no_path)
