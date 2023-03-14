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
    layerset_list = []

    def fun_递归编组(self, layer_sets: CDispatch):
        for in_layer in layer_sets.Layers:

            if in_layer.LayerType == LayerType.LayerSet:
                in_layer.Name = f'编组 {in_layer.id}'
                self.layerset_list.append(in_layer)
                self.fun_递归编组(in_layer)

            else:
                if self.fun_删除包含名称广告图层(in_layer) is True:
                    if self.fun_删除等于名称广告图层(in_layer) is True:
                        visible = in_layer.Visible
                        if in_layer.Kind != 2:
                            in_layer.Name = f'图层 {in_layer.id}'
                        else:
                            in_layer.Name = in_layer.TextItem.Contents

                        in_layer.Unlink()
                        in_layer.Visible = visible

                        self.artlayer_list.append(in_layer)

    def fun_构建列表(self):
        self.fun_递归编组(self.doc)

    def fun_删除包含名称广告图层(self, in_layer: CDispatch):
        for name in self.ad_name_list.include_name_list:
            if name in str(in_layer.Name).lower():
                print('\n删除广告图层：', in_layer.Name, '\n')
                in_layer.AllLocked = True
                in_layer.AllLocked = False
                in_layer.Delete()
                return False

        return True

    def fun_删除等于名称广告图层(self, in_layer: CDispatch):
        for name in self.ad_name_list.is_name_list:
            if str(in_layer.Name).lower() == name:
                print('\n删除广告图层：', in_layer.Name, '\n')
                in_layer.AllLocked = True
                in_layer.AllLocked = False
                in_layer.Delete()
                return False

        return True

    def run_处理所有图层(self):
        self.fun_构建列表()


if __name__ == '__main__':
    from win32com.client import Dispatch

    app = Dispatch('photoshop.application')
    app.Open(r'E:\小夕素材\9000-9999\9291\9291\小夕素材(14).psd')
    d = app.ActiveDocument
    rl = RecursiveLayers(d)
    rl.run_处理所有图层()
