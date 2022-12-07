import shutil
from functools import cached_property
from pathlib import Path
from typing import Optional
from tqdm import tqdm
from module_素材处理.core.setting import IMAGE_FILE_SUFFIX
from module_素材处理.core.setting import MATERIAL_FILE_SUFFIX
from module_素材处理.core.素材文件夹功能 import MaterialFolderStructure
from module_素材处理.core.素材文件夹功能.fun_指定遍历 import fun_指定遍历
from module_素材处理.core.素材文件夹功能.fun_获取数字 import fun_获取数字


class MaterialDirMerge:
    def __init__(self, ori_path: str, dst_path: str, tb_name: str):
        self.ori_path = MaterialFolderStructure(root_path=ori_path)
        self.dst_path = MaterialFolderStructure(root_path=dst_path)
        self.tb_name = tb_name

    @cached_property
    def fun_获取最大文件数(self) -> int:
        all_file = fun_指定遍历(self.dst_path.material_path, MATERIAL_FILE_SUFFIX)
        all_file.sort(key=lambda k: fun_获取数字(k))

        num = fun_获取数字(all_file[-1])
        return int(num)

    @staticmethod
    def fun_根据源文件获取图片(material_file_path: Path) -> Optional[Path]:
        for img_suffix in IMAGE_FILE_SUFFIX:
            img_file_path = material_file_path.with_suffix(img_suffix)
            if img_file_path.exists() is True:
                return img_file_path

        return None

    def fun_根据素材图获取预览图(self, material_img_path: Path) -> Path:
        in_file_parts = list(material_img_path.parts)
        ori_parts = list(self.ori_path.material_path.parts)
        dst_parts = list(self.ori_path.preview_path.parts)

        in_file_parts[:len(ori_parts)] = dst_parts
        prev_img_path = Path('\\'.join(in_file_parts))
        return prev_img_path

    def main(self):
        num = self.fun_获取最大文件数 + 1
        all_file = fun_指定遍历(self.ori_path.material_path, MATERIAL_FILE_SUFFIX)
        for in_file in tqdm(all_file, desc='移动文件', ncols=100):
            in_file: Path

            # 源文件
            dst_file_path = self.dst_path.material_path / f'{self.tb_name}({num}){in_file.suffix.lower()}'
            shutil.move(in_file, dst_file_path)
            print(dst_file_path)

            # 素材图片
            in_file_img_path = self.fun_根据源文件获取图片(in_file)
            if in_file_img_path is not None:
                dst_img_path = self.dst_path.material_path / f'{self.tb_name}({num}){in_file_img_path.suffix.lower()}'
                shutil.move(in_file_img_path, dst_img_path)
                print(dst_img_path)

                # 预览图
                prev_img_path = self.fun_根据素材图获取预览图(in_file_img_path)
                if prev_img_path.exists() is True:
                    dst_prev_path = self.dst_path.preview_path / f'{self.tb_name}({num}){prev_img_path.suffix.lower()}'
                    shutil.move(prev_img_path, dst_prev_path)
                    print(dst_prev_path)

            print('\n')

            num += 1

        print(f'删除源文件夹:{self.ori_path.root_path}')
        shutil.rmtree(self.ori_path.root_path)


if __name__ == '__main__':
    md = MaterialDirMerge(
        ori_path=r'G:\DOWN\新建文件夹 元旦++',
        dst_path=r'E:\小夕素材\9000-9999\9257',
        tb_name='小夕素材'
    )
    md.main()
