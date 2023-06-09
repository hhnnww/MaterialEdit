import shutil
from pathlib import Path

import pythoncom
from PIL import Image
from pydantic import BaseModel
from tqdm import tqdm

from module_素材处理.core.setting import AD_FILE_SUFFIX
from module_素材处理.core.setting import IMAGE_FILE_SUFFIX
from module_素材处理.core.setting import IMG_PATH
from module_素材处理.core.图片编辑 import PICEdit
from module_素材处理.core.素材文件夹功能 import MaterialFolderFunction
from module_素材处理.core.素材文件夹功能 import MaterialFolderStructure
from module_素材处理.core.素材文件夹功能.PSFile3.fun_对比所有导出的图片 import fun_所有广告图片
from module_素材处理.core.素材文件夹功能.PSFile3.fun_导出图层PNG import fun_清空OUT_PATH


class ItemIn(BaseModel):
    root_path: str
    tb_name: str
    action_name: str


class MaterialPathAction:
    def __init__(self, item_in: ItemIn):
        self.item_in = item_in

        self.ma_path = MaterialFolderStructure(root_path=item_in.root_path)
        self.ma_func = MaterialFolderFunction

    def fun_制作文件夹预览(self):
        self.ma_func.fun_制作文件夹预览(in_path=self.ma_path.material_path).main()

    def fun_素材图蜘蛛水印(self):
        self.ma_func.fun_素材图蜘蛛水印(in_path=self.ma_path.material_path, tb_name=self.item_in.tb_name)

    def fun_生成SKP批量导出脚本(self):
        self.ma_func.fun_生成SKP批量导出脚本(in_path=self.ma_path.material_path)

    def fun_按数字分类(self):
        self.ma_func.fun_按数字分类(in_path=self.ma_path.material_path).main()
        self.ma_func.fun_按数字分类(in_path=self.ma_path.preview_path).main()

    def fun_字体生成图片(self):
        for in_file in tqdm(self.ma_func.fun_指定遍历(self.ma_path.material_path, ['.otf', '.ttf']), ncols=100,
                            desc='字体生成图片'):
            try:
                self.ma_func.fun_字体生成图片(font_path=in_file, tb_name=self.item_in.tb_name).main()
            except:
                pass

    def fun_按格式分类(self):
        self.ma_func.fun_按格式分类(self.ma_path.material_path).main()

    def fun_移动到根目录(self):
        self.ma_func.fun_移动到根目录(self.ma_path.material_path)

        if self.ma_path.preview_path.exists() is True:
            self.ma_func.fun_移动到根目录(self.ma_path.preview_path)

    def fun_删除广告文件(self):
        for in_file in self.ma_func.fun_指定遍历(self.ma_path.material_path, AD_FILE_SUFFIX):
            in_file.unlink()

        for in_file in self.ma_path.material_path.rglob('*'):
            if in_file.is_file():

                if in_file.stat().st_size < 8000:
                    in_file.unlink()

                if '扫码进店免费领取资料' in in_file.stem and in_file.suffix.lower() == '.jpg':
                    in_file.unlink()

    def fun_解压ZIP(self):
        self.ma_func.fun_解压ZIP(in_path=self.ma_path.material_path)

    def fun_文件重命名(self):
        self.ma_func.fun_文件重命名(self.ma_path.material_path, 'test')
        self.ma_func.fun_文件重命名(self.ma_path.material_path, self.item_in.tb_name)

        if self.ma_path.preview_path.exists() is True:
            self.ma_func.fun_文件重命名(self.ma_path.preview_path, 'test')
            self.ma_func.fun_文件重命名(self.ma_path.preview_path, self.item_in.tb_name)

    def fun_复制到预览图(self):
        self.ma_func.fun_复制图片到指定目录(self.ma_path.material_path, self.ma_path.preview_path)

    def fun_复制到效果图(self):
        self.ma_func.fun_复制图片到指定目录(self.ma_path.material_path, self.ma_path.effect_path, rename=True)
        for in_file in self.ma_func.fun_指定遍历(self.ma_path.material_path, IMAGE_FILE_SUFFIX):
            if in_file.is_file():
                in_file.unlink()

    @staticmethod
    def fun_has_img(in_file: Path):
        for img_suffix in IMAGE_FILE_SUFFIX:
            img_path = in_file.with_suffix(img_suffix)
            if img_path.exists() is True:
                return True

        return False

    def fun_PSD删广告生成图片(self):
        fun_清空OUT_PATH()
        ad_pic_list = fun_所有广告图片()

        pythoncom.CoInitialize()
        for in_file in tqdm(self.ma_func.fun_指定遍历(self.ma_path.material_path, ['.psd', '.psb']), ncols=100,
                            desc='PSD删除广告生成图片'):

            if self.fun_has_img(in_file) is False:
                self.ma_func.fun_PS3操作(ps_path=in_file.as_posix(),
                                         tb_name=self.item_in.tb_name, ad_pic_list=ad_pic_list).run_删除广告导出PNG()

        pythoncom.CoUninitialize()

    def fun_PSD添加广告生成图片(self):
        pythoncom.CoInitialize()
        for in_file in tqdm(self.ma_func.fun_指定遍历(self.ma_path.material_path, ['.psd', '.psb']), ncols=100,
                            desc='PSD添加广告生成图片'):

            if self.fun_has_img(in_file) is False:
                ps_obj = self.ma_func.fun_PS操作.open(in_file.as_posix(), tb_name=self.item_in.tb_name,
                                                      ad_pic_list=self.ma_func.fun_PS广告图片())
                ps_obj.run_导出_加广告()

        pythoncom.CoUninitialize()

    def fun_PSD生成图片(self):
        pythoncom.CoInitialize()
        for in_file in tqdm(self.ma_func.fun_指定遍历(self.ma_path.material_path, ['.psd', '.psb']), ncols=100,
                            desc='PSD生成图片'):

            if self.fun_has_img(in_file) is False:
                ps_obj = self.ma_func.fun_PS操作.open(in_file.as_posix(), tb_name=self.item_in.tb_name,
                                                      ad_pic_list=self.ma_func.fun_PS广告图片())
                ps_obj.run_导出()

        pythoncom.CoUninitialize()

    def fun_AI导出图片(self):
        pythoncom.CoInitialize()
        for in_file in tqdm(self.ma_func.fun_指定遍历(self.ma_path.material_path, ['.ai', '.eps']), ncols=100,
                            desc='AI导出PNG'):

            if self.fun_has_img(in_file) is False:
                ai_file = self.ma_func.fun_AI操作(file=in_file, tb_name=self.item_in.tb_name)
                ai_file.main()

        pythoncom.CoUninitialize()

    def fun_PPT导出图片(self):
        pythoncom.CoInitialize()

        for in_file in tqdm(self.ma_func.fun_指定遍历(self.ma_path.material_path, ['.ppt', '.pptx']), ncols=100,
                            desc='PPT导出PNG'):

            if self.fun_has_img(in_file) is False:
                self.ma_func.fun_PPT操作(ppt_path=in_file, ppt_export_path=self.ma_path.effect_path).main()

        pythoncom.CoUninitialize()

    def fun_素材图片添加水印(self):
        water_pil = Image.open(
            (IMG_PATH / self.item_in.tb_name / 'site_logo.png').as_posix()
        )
        water_pil.thumbnail((150, 150), 1)
        padding = 30
        for in_file in tqdm(self.ma_func.fun_指定遍历(self.ma_path.material_path, IMAGE_FILE_SUFFIX),
                            desc='图片添加水印', ncols=100):
            with Image.open(in_file.as_posix()) as im:
                if 1500 not in im.size:
                    im.thumbnail((1500, 1500), 1)
                    top = im.height - water_pil.height - padding
                    im.paste(water_pil, (padding, top), water_pil)
                    im.save(in_file.as_posix())
                else:
                    print('边距 1500 不添加')

    def fun_删除所有(self):
        shutil.rmtree(self.ma_path.root_path)

    def fun_删除素材图片(self):
        for in_file in self.ma_func.fun_指定遍历(self.ma_path.material_path, IMAGE_FILE_SUFFIX):
            in_file.unlink()

    def fun_删除效果图(self):
        if self.ma_path.effect_path.exists() is True:
            shutil.rmtree(self.ma_path.effect_path)

    def fun_删除预览图(self):
        if self.ma_path.preview_path.exists() is True:
            shutil.rmtree(self.ma_path.preview_path)

    def fun_删除所有EPS(self):
        for in_file in self.ma_func.fun_指定遍历(self.ma_path.material_path, ['.eps']):
            in_file.unlink()

    def fun_删除图片边框(self):
        for in_file in tqdm(self.ma_func.fun_指定遍历(self.ma_path.material_path, IMAGE_FILE_SUFFIX),
                            desc='删除图片边框', ncols=100):
            in_file: Path
            print(f'处理：{in_file.as_posix()}')

            im = Image.open(in_file.as_posix())
            im = PICEdit.fun_边框删除(im, None).main()
            im.save(in_file.as_posix())

    def fun_删除相同文件(self):
        self.ma_func.fun_删除相同文件(in_path=self.ma_path.material_path).main()

    def fun_全自动一键操作(self):
        self.fun_移动到根目录()
        self.fun_复制到效果图()
        self.fun_解压ZIP()
        self.fun_移动到根目录()
        self.fun_复制到效果图()
        self.fun_删除广告文件()
        self.fun_删除素材图片()
        self.fun_文件重命名()

        self.fun_PSD添加广告生成图片()
        self.fun_AI导出图片()
        self.fun_PPT导出图片()

        self.fun_复制到预览图()
        self.fun_素材图片添加水印()

    def fun_压缩为RAR(self):
        self.ma_func.fun_压缩为RAR(in_path=self.ma_path.material_path, suffix=['.otf', '.ttf'])

    def fun_享设计文件夹改名(self):
        self.ma_func.fun_享设计文件夹改名(in_path=self.ma_path.material_path, tb_name=self.item_in.tb_name).main()
