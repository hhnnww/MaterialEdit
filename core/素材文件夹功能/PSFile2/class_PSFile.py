import time
from pathlib import Path

import face_recognition
from win32com.client import Dispatch

from core.素材文件夹功能.PSFile2.fun_2_导出所有图层 import run_导出所有图层
from core.素材文件夹功能.PSFile2.fun_3_对比所有图片 import fun_打开图片, run_对比所有图片, fun_所有广告图片
from core.素材文件夹功能.PSFile2.fun_4_导出PNG import export_png
from core.素材文件夹功能.PSFile2.fun_5_插入广告 import fun_插入广告
from core.素材文件夹功能.PSFile2.fun_6_文字图层替换 import fun_文字图层替换内容
from core.素材文件夹功能.PSFile2.fun_PS基础操作 import fun_选择图层
from core.素材文件夹功能.PSFile2.fun_清除和添加注释 import fun_清理注释
from core.素材文件夹功能.PSFile2.fun_高斯模糊 import gaussianBlur_0


class PSFile:
    app = None
    doc = None
    file = None
    tb_name = None
    ad_layer_name = '隐藏 或 删除此图层即可开始您的编辑.'
    ad_pic_list = []

    @classmethod
    def open(cls, ps_file: str, tb_name: str, ad_pic_list: list):
        ps_cla = cls()
        app = Dispatch('Photoshop.Application')
        app.Open(ps_file)
        ps_cla.app = app
        ps_cla.doc = ps_cla.app.ActiveDocument
        app.displayDialogs = 3

        ps_cla.file = Path(ps_file)
        ps_cla.tb_name = tb_name
        ps_cla.ad_pic_list = ad_pic_list

        fun_清理注释(app=app)
        return ps_cla

    def fun_删除广告(self):
        all_item = run_导出所有图层(in_doc=self.doc, file=self.file)
        art_item_list = all_item[0]
        text_item_list = all_item[1]

        # 删除图形图层广告
        for item in art_item_list:
            img_path = item.get('img_path')

            if img_path.exists() is True:

                while img_path.stat().st_size == 0:
                    time.sleep(1)

                img = fun_打开图片(img_path.as_posix())
                res = run_对比所有图片(img, self.ad_pic_list)

                if res is True:
                    print(f'删除广告图层：{item.get("item").Name}')
                    if item.get('item').AllLocked is True:
                        item.get('item').AllLocked = False

                    item.get('item').Delete()

                else:
                    image = face_recognition.load_image_file(img_path.as_posix())
                    face_location = face_recognition.face_locations(image)
                    if len(face_location) > 0:
                        fun_选择图层(app=self.app, item=item.get('item'))
                        gaussianBlur_0(app=self.app)

        # 替换文字图层内容
        for item in text_item_list:
            fun_文字图层替换内容(item)

    def fun_导出PNG(self):
        print('导出PNG')
        export_png(
            file=self.file, ref_doc=self.doc, ad_layer_name=self.ad_layer_name
        )

    def fun_插入广告(self):
        print('插入广告')
        fun_插入广告(app=self.app, doc=self.doc, tb_name=self.tb_name, ad_layer_name=self.ad_layer_name)

    def run_删广告_导出_加广告(self):
        self.fun_删除广告()
        self.fun_导出PNG()
        self.fun_插入广告()
        self.doc.Save()
        self.doc.Close(2)

    def run_导出_加广告(self):
        self.fun_导出PNG()
        self.fun_插入广告()
        self.doc.Save()
        self.doc.Close(2)

    def run_导出(self):
        self.fun_导出PNG()
        self.doc.Close(2)


if __name__ == '__main__':
    ad_list = fun_所有广告图片()


    def fun_处理PSD(ps_file: str):
        psf = PSFile.open(ps_file, '小夕素材', ad_list)
        psf.run_删广告_导出_加广告()


    def fun_处理文件夹(dir_path: Path):
        for in_file in dir_path.iterdir():
            png_path = in_file.with_suffix('.png')
            if in_file.is_file():
                if in_file.suffix.lower() in ['.psd']:
                    if png_path.exists() is False:
                        print(f'\n处理:{in_file}')
                        # fun_处理PSD(in_file.as_posix())
                        psf = PSFile.open(in_file.as_posix(), '小夕素材', ad_list)
                        export_png(ref_doc=psf.doc, file=psf.file, ad_layer_name=psf.ad_layer_name, del_ad_layer=False)
                        psf.doc.Close(2)


    fun_处理PSD(
        r'E:\DOWN\新建文件夹\新建文件夹\小夕素材(17).psd'
    )
