from functools import cached_property
from pathlib import Path
from pprint import pprint

from module_素材处理.core.setting import MATERIAL_FILE_SUFFIX
from module_素材处理.core.素材文件夹信息.fun_尺寸转换 import fun_尺寸转换
from module_素材处理.core.素材文件夹功能.fun_指定遍历 import fun_指定遍历


class MaterialInfo:
    """
    输入素材文件夹
    获取素材文件夹里面的信息
    """

    def __init__(self, in_path: str):
        self.path = Path(in_path)

    @cached_property
    def all_file(self):
        all_file = [in_file for in_file in self.path.rglob('*') if in_file.is_file()]
        return all_file

    @cached_property
    def all_material_file(self):
        return fun_指定遍历(self.path, MATERIAL_FILE_SUFFIX)

    @cached_property
    def pro_素材格式(self) -> str:
        material_format = []
        for in_file in self.all_material_file:
            suffix = in_file.suffix.upper().replace('.', '')
            if suffix not in material_format:
                material_format.append(suffix)

        return material_format

    @cached_property
    def pro_文件夹尺寸(self) -> str:
        all_size = sum([in_file.stat().st_size for in_file in self.all_file])
        return fun_尺寸转换(all_size)

    @cached_property
    def pro_源文件列表(self) -> str:
        ma_format = ''
        for maf in MATERIAL_FILE_SUFFIX:
            ma_count = len([in_file for in_file in self.all_material_file if in_file.suffix.lower() == maf])
            if ma_count > 0:
                ma_format += f'{ma_count}个{maf.replace(".", "").upper()}素材 '

        return ma_format


if __name__ == '__main__':
    mi = MaterialInfo(r'G:\饭桶设计\0-999\0055\0055')
    pprint(mi.all_file)
    pprint(' '.join(mi.pro_素材格式))
    pprint(mi.pro_文件夹尺寸)
    pprint(mi.pro_源文件列表)
