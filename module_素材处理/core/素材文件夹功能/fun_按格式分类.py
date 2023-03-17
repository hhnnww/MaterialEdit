from pathlib import Path
from module_素材处理.core.setting import MATERIAL_FILE_SUFFIX


class CateBySuffix:
    def __init__(self, in_path: Path):
        self.in_path = in_path

    @staticmethod
    def fun_获取STEM(in_file: Path):
        stem = in_file.suffix
        stem = stem.replace('.', '')
        stem = stem.upper()
        return stem

    def fun_构建文件目录(self, in_file: Path):
        stem = self.fun_获取STEM(in_file)
        path = self.in_path / stem

        if path.exists() is False:
            path.mkdir()

        return path

    def main(self):
        for in_file in self.in_path.rglob('*'):
            if in_file.is_file():
                in_file_path = self.fun_构建文件目录(in_file)

                if in_file.parent == in_file_path:
                    continue

                new_name = in_file_path / in_file.name

                if new_name.exists() is False:

                    # in_file_png_path = in_file.with_suffix('.png')
                    # if in_file_png_path.exists() is True:
                    #     in_file_png_path_new = in_file_path / in_file_png_path.name
                    #     if in_file_png_path_new.exists() is False:
                    #         in_file_png_path.rename(in_file_png_path_new)

                    in_file.rename(new_name)


if __name__ == '__main__':
    CateBySuffix(Path(r'G:\饭桶设计\1000-1999\1015\1015')).main()
