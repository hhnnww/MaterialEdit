import math
import re
import shutil
from pathlib import Path


class CateByNum:
    def __init__(self, in_path: Path):
        self.in_path = in_path

    @staticmethod
    def fun_获取NUM(in_path: Path):
        num_list = re.findall('\d+', in_path.stem)
        if len(num_list) > 0:
            return int(num_list[0])

        return 0

    def fun_根据NUM获取文件夹(self, num: int):
        start_num = str(math.floor(num / 100)) + '00'
        end_num = str(math.floor(num / 100)) + '99'
        num_path = self.in_path / f'{start_num}_{end_num}'
        if num_path.exists() is False:
            num_path.mkdir(parents=True)

        return num_path

    def main(self):
        num_path_list = []
        for in_file in self.in_path.rglob('*'):
            if in_file.is_file():
                num = self.fun_获取NUM(in_file)
                num_path = self.fun_根据NUM获取文件夹(num)

                if in_file.parent != num_path:
                    new_path = num_path / in_file.name
                    in_file.rename(new_path)

                num_path_list.append(num_path)

        for in_file in self.in_path.iterdir():
            if in_file.is_dir() and in_file not in num_path_list:
                shutil.rmtree(in_file)


if __name__ == '__main__':
    cbn = CateByNum(Path(r'E:\小夕素材\9000-9999\9261\9261'))
    cbn.main()
