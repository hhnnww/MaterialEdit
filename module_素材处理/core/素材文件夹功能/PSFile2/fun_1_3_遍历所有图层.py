from dataclasses import dataclass

from win32com.client import CDispatch

from module_素材处理.core.素材文件夹功能.PSFile2.open_yaml import ADNameList


@dataclass
class LayerType:
    LayerSet: int = 2
    ArtLayer: int = 1


class RecursiveLayers:
    def __init__(self, doc: CDispatch):
        self.doc = doc
        self.run_处理所有图层()

    ad_name_list = ADNameList
    artlayer_list = []

    @staticmethod
    def fun_修改图层名字(in_layer, name: str):
        if in_layer.Name != name:
            visible = in_layer.Visible
            in_layer.Name = name

            in_layer.Unlink()
            in_layer.Visible = visible

    def fun_处理图层名字(self, in_layer):
        if in_layer.Kind != 2:
            self.fun_修改图层名字(in_layer, f'图层 {in_layer.id}')
        else:
            self.fun_修改图层名字(in_layer, in_layer.TextItem.Contents)

    def fun_递归编组(self, layer_sets: CDispatch):
        for in_layer in layer_sets.Layers:
            in_layer.AllLocked = True
            in_layer.AllLocked = False

            if in_layer.LayerType == LayerType.LayerSet:
                in_layer.Name = f'编组 {in_layer.id}'
                in_layer.AllLocked = False
                self.fun_递归编组(in_layer)

            else:
                if self.fun_删除包含名称广告图层(in_layer) is True:
                    if self.fun_删除等于名称广告图层(in_layer) is True:
                        self.fun_处理图层名字(in_layer)
                        self.artlayer_list.append(in_layer)

    @staticmethod
    def fun_删除图层(in_layer):
        print('\n删除广告图层：', in_layer.Name, '\n')

        if in_layer.AllLocked is True:
            in_layer.AllLocked = False

        in_layer.Delete()

    def fun_删除包含名称广告图层(self, in_layer: CDispatch):
        for name in self.ad_name_list.include_name_list:
            if str(name).lower() in str(in_layer.Name).lower():
                self.fun_删除图层(in_layer)
                return False
        return True

    def fun_删除等于名称广告图层(self, in_layer: CDispatch):
        for name in self.ad_name_list.is_name_list:
            if str(in_layer.Name).lower() == str(name).lower():
                self.fun_删除图层(in_layer)
                return False
        return True

    def run_处理所有图层(self):
        self.fun_递归编组(self.doc)


if __name__ == '__main__':
    from win32com.client import Dispatch
    from pprint import pprint

    app = Dispatch('photoshop.application')
    # app.Open(r'E:\小夕素材\9000-9999\9291\9291\小夕素材(14).psd')
    d = app.ActiveDocument
    rl = RecursiveLayers(d)
    pprint([l.Name for l in rl.artlayer_list])
