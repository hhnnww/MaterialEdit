import time
from pathlib import Path

import face_recognition
from win32com.client import Dispatch

from module_素材处理.core.素材文件夹功能.PSFile2.fun_2_导出所有图层 import run_导出所有图层
from module_素材处理.core.素材文件夹功能.PSFile2.fun_3_对比所有图片 import fun_所有广告图片
from module_素材处理.core.素材文件夹功能.PSFile2.fun_3_对比所有图片 import fun_打开图片
from module_素材处理.core.素材文件夹功能.PSFile2.fun_3_对比所有图片 import run_对比所有图片
from module_素材处理.core.素材文件夹功能.PSFile2.fun_4_导出PNG import export_png
from module_素材处理.core.素材文件夹功能.PSFile2.fun_5_插入广告 import fun_插入广告
from module_素材处理.core.素材文件夹功能.PSFile2.fun_6_文字图层替换 import fun_文字图层替换内容
from module_素材处理.core.素材文件夹功能.PSFile2.fun_PS基础操作 import fun_选择图层
from module_素材处理.core.素材文件夹功能.PSFile2.fun_PS基础操作 import select_0
from module_素材处理.core.素材文件夹功能.PSFile2.fun_清除和添加注释 import fun_清理注释
from module_素材处理.core.素材文件夹功能.PSFile2.fun_高斯模糊 import gaussianBlur_0
from module_素材处理.core.素材文件夹功能.PSFile2.open_yaml import open_yml


class PSFile:
    app = None
    doc = None
    file = None
    tb_name = None
    ad_layer_name = '隐藏 或 删除此图层即可开始您的编辑.'
    ad_pic_list = []

    @classmethod
    def open(cls, ps_file: str, tb_name: str, ad_pic_list: list):
        print(f'\n\n处理文件:{ps_file}')
        ps_cla = cls()
        app = Dispatch('Photoshop.Application')
        try:
            app.Open(ps_file)
        except Exception as err:
            print(err)
            return False

        ps_cla.app = app
        ps_cla.doc = ps_cla.app.ActiveDocument
        app.displayDialogs = 3

        ps_cla.file = Path(ps_file)
        ps_cla.tb_name = tb_name
        ps_cla.ad_pic_list = ad_pic_list

        fun_清理注释(app=app)
        select_0(app=app, doc=ps_cla.doc)
        return ps_cla

    def fun_删除广告(self):
        all_item = run_导出所有图层(in_doc=self.doc, file=self.file)
        art_item_list = all_item[0]
        text_item_list = all_item[1]

        # 删除图形图层广告
        for item in art_item_list:
            img_path = item.get('img_path')
            if img_path.exists() is True:
                print(f'对比图层：{item.get("item").Name}')

                # 设置图片导出超时时间，太长了就不等了。
                time_out = 0
                time_out_state = False
                while img_path.stat().st_size == 0:
                    time.sleep(1)
                    time_out += 1

                    if time_out >= 60:
                        time_out_state = True
                        break

                if time_out_state is True:
                    continue

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
        ad_layers_list = open_yml().get('export_name_list')
        layer_list = []

        for art_layer in self.doc.ArtLayers:
            layer_list.append(art_layer)

        for art_layer in layer_list:
            art_layer_name = str(art_layer.Name).lower()

            for ad_name in ad_layers_list:

                ad_name = ad_name.lower()

                if ad_name in art_layer_name:
                    if art_layer.AllLocked is True:
                        art_layer.AllLocked = False

                    art_layer.Delete()

        self.fun_导出PNG()
        self.fun_插入广告()
        self.doc.Save()
        self.doc.Close(2)

    def run_导出(self):
        self.fun_导出PNG()
        self.doc.Close(2)


if __name__ == '__main__':
    psf = PSFile.open(ps_file=r'F:\小夕素材\520促销\520促销\小夕素材(1).psd', tb_name='小夕素材',
                      ad_pic_list=fun_所有广告图片())

    psf.run_删广告_导出_加广告()
