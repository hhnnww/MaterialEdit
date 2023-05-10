from pathlib import Path
from typing import List

from win32com.client import CDispatch
from win32com.client import Dispatch

from module_素材处理.core.素材文件夹功能.PSFile3.fun_导出PNG import com_psd导出png
from module_素材处理.core.素材文件夹功能.PSFile3.fun_插入广告 import fun_插入广告
from module_素材处理.core.素材文件夹功能.PSFile3.fun_文字图层替换广告 import com_文字图层广告
from module_素材处理.core.素材文件夹功能.PSFile3.fun_普通图层替换广告 import com_普通图层广告
from module_素材处理.core.素材文件夹功能.PSFile3.model import IncludeName
from module_素材处理.core.素材文件夹功能.PSFile3.model import IsName
from module_素材处理.core.素材文件夹功能.PSFile3.model import TextReplaceName, IsPhoto
from module_素材处理.core.素材文件夹功能.PSFile3.model import database


class LayerType:
    ArtLayer = 1
    LayerSet = 2


class ArtLayerKind:
    TextLayer = 2


class PSFile:
    def __init__(self, ps_path: str, tb_name: str):
        self.ps_path = ps_path
        self.tb_name = tb_name

        self.app = Dispatch('photoshop.application')
        self.app.displayDialogs = 3

        self.app.Open(ps_path)
        self.doc = self.app.ActiveDocument

        self.ad_layer_name = '隐藏 或 删除此图层即可开始您的编辑.'

    @staticmethod
    def get_all_layer(in_object: CDispatch):
        """
        获取所有的图层
        :param in_object:
        :return:
        """
        in_layer_list = []
        for in_layer in in_object.layers:
            try:
                print(f'归递图层：\t{in_layer.Name}')
            except:
                pass

            visible = in_layer.Visible
            if in_layer.AllLocked is True:
                in_layer.AllLocked = False
                in_layer.Visible = visible

            if in_layer.LayerType == LayerType.LayerSet:
                in_layer_list.extend(PSFile.get_all_layer(in_layer))

            elif in_layer.LayerType == LayerType.ArtLayer:
                in_layer_list.append(in_layer)

        return in_layer_list

    @staticmethod
    def get_all_layer_set(in_object: CDispatch):
        """
        获取所有的编组
        :param in_object:
        :return:
        """
        in_layer_set_list = []
        for in_layer in in_object.LayerSets:
            visible = in_layer.Visible
            print(f'归递编组：\t{in_layer.Name}')

            if in_layer.AllLocked is True:
                in_layer.AllLocked = False
                in_layer.Visible = visible

            in_layer_set_list.append(in_layer)
            in_layer_set_list.extend(PSFile.get_all_layer_set(in_layer))

        return in_layer_set_list

    def com_删除广告图层(self, all_layers: List[CDispatch]):
        """
        从数据库获取所有广告语
        根据图层名字删除所有的广告图层
        :param all_layers:
        :return:
        """
        with database:
            include_names: List[IncludeName] = list(IncludeName.select())
            is_names: List[IsName] = list(IsName.select())
            text_replace: List[TextReplaceName] = list(TextReplaceName.select())
            photo_names: List[IsPhoto] = list(IsPhoto.select())

        for in_layer in all_layers:
            # 普通图层
            if in_layer.Kind != ArtLayerKind.TextLayer:
                com_普通图层广告(self.app, in_layer, include_names, is_names, photo_names)

            # 文字图层
            else:
                com_文字图层广告(in_layer, text_replace)

    @staticmethod
    def com_修改所有编组(all_layer_sets: List[CDispatch]):
        for layer_set in all_layer_sets:
            visible = layer_set.Visible
            layer_set.Name = f'组 {layer_set.ID}'
            layer_set.Visible = visible

    def run_删除广告导出PNG(self):
        all_layer_sets = self.get_all_layer_set(self.doc)
        all_layers = self.get_all_layer(self.doc)
        self.com_删除广告图层(all_layers)
        self.com_修改所有编组(all_layer_sets)

        save_path = Path(self.ps_path)
        print(f'导出PNG:\t{save_path.with_suffix(".png")}')

        com_psd导出png(
            ref_doc=self.doc,
            file=save_path,
            ad_layer_name=''
        )
        fun_插入广告(self.app, self.doc, self.tb_name, self.ad_layer_name)

        print(f'保存：\t{save_path.as_posix()}')
        self.doc.Save()

        print(f'关闭：\t{save_path.as_posix()}')
        self.doc.Close(2)


if __name__ == '__main__':
    ps = PSFile(
        ps_path=r'F:\小夕素材\10000-10999\10047\10047\小夕素材(14).psd',
        tb_name='小夕素材'
    )

    ps.run_删除广告导出PNG()
