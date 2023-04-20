from pathlib import Path


class XiangDesignPathRename:
    def __init__(self, in_path: Path, tb_name: str):
        self.in_path = in_path
        self.tb_name = tb_name

    def can_rename(self, ma_in_path: Path):
        if ma_in_path.is_dir():
            if self.tb_name not in ma_in_path.stem:
                return True

        return False

    def get_new_path(self, ma_in_path: Path, num: int):
        new_stem = f'{self.tb_name}({num})'
        new_path = ma_in_path.with_stem(new_stem)
        return new_path

    @staticmethod
    def has_ai_file(ma_in_path: Path):
        ai_file_list = []
        for in_file in ma_in_path.iterdir():
            if in_file.is_file() and in_file.suffix.lower() == '.ai':
                ai_file_list.append(in_file)

        if len(ai_file_list) == 1:
            return True

        return False

    @staticmethod
    def get_ai_file(ma_in_path: Path):
        for in_file in ma_in_path.iterdir():
            if in_file.is_file() and in_file.suffix.lower() == '.ai':
                return in_file

    def main(self):
        num = 1
        for ma_in_path in self.in_path.iterdir():
            if self.can_rename(ma_in_path):
                new_path = self.get_new_path(ma_in_path, num)
                if new_path.exists() is False:
                    ai_file = self.get_ai_file(ma_in_path)
                    new_ai_file = ai_file.with_stem(f'{self.tb_name}({num})')

                    # AI文件先改名
                    if new_ai_file.exists() is False:
                        print(ai_file, "\t-->\t", new_ai_file)
                        ai_file.rename(new_ai_file)

                        # 文件夹后改名
                        print(ma_in_path, "\t-->\t", new_path)
                        ma_in_path.rename(new_path)

                        num += 1

        return True


if __name__ == '__main__':
    rename = XiangDesignPathRename(
        in_path=Path(r'X:\H000-H999\H0612\H0612'),
        tb_name='饭桶设计'
    )

    rename.main()
