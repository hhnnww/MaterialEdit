import filecmp
from itertools import combinations
from pathlib import Path
from typing import Tuple


class DelSameFile:
    def __init__(self, in_path: Path):
        self.in_path = in_path

    def all_file_comb(self):
        all_file = []
        for in_file in self.in_path.rglob('*'):
            if in_file.is_file():
                all_file.append(in_file)

        re_comb_list = []

        comb_list = list(combinations(all_file, 2))
        for in_comb in comb_list:
            in_comb: Tuple[Path, Path]
            if in_comb[0].suffix.lower() == in_comb[1].suffix.lower():
                re_comb_list.append(in_comb)

        return re_comb_list

    @staticmethod
    def is_same_file(in_comb_list: Tuple[Path, Path]):
        if in_comb_list[0].exists() is True and in_comb_list[1].exists() is True:
            return filecmp.cmp(f1=in_comb_list[0].as_posix(), f2=in_comb_list[1].as_posix())

        return False

    def main(self):
        for single_comb_list in self.all_file_comb():
            single_comb_list: Tuple[Path, Path]
            if self.is_same_file(single_comb_list):
                print(f'删除第二个文件: {single_comb_list[1].as_posix()}')
                single_comb_list[1].unlink()


if __name__ == '__main__':
    dsf = DelSameFile(
        in_path=Path(r'G:\饭桶设计\1000-1999\1851\1851')
    )
    dsf.main()
