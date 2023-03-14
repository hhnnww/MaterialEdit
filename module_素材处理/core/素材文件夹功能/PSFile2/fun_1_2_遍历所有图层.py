from win32com.client import CDispatch

from module_素材处理.core.素材文件夹功能.PSFile2.open_yaml import open_yml

yaml_dict = open_yml()


class GetAllLayer:
    def __init__(self, in_doc: CDispatch):
        self.in_doc = in_doc
        self.layer_list = []
        self.set_list = []

        self.run_构建所有编组()
        self.run_构建所有图层()

        # self.run_处理所有编组和图层()

    @staticmethod
    def fun_判断图层名字来删除广告(in_layer: CDispatch):
        # 如果包含
        ad_name_include = yaml_dict.get('include_name_list')
        in_layer.AllLocked = True
        in_layer.AllLocked = False

        for ad_layer_name_single in ad_name_include:
            if in_layer.LayerType == 1:
                if in_layer.Kind != 2:
                    if ad_layer_name_single in in_layer.Name.lower():
                        print(f'删除图层:{in_layer.Name}')
                        in_layer.Delete()
                        return False

        # 如果等于
        ad_name_is = yaml_dict.get('is_name_list')
        if in_layer.LayerType == 1 and in_layer.Kind != 2:
            if in_layer.Name.lower() in ad_name_is:
                print(f'删除图层:{in_layer.Name}')
                in_layer.Delete()
                return False

        return True

    @staticmethod
    def fun_修改图层和编组名字(in_layer):
        layer_prefix = ''
        if in_layer.LayerType == 1:
            layer_prefix = '图层'
        elif in_layer.LayerType == 2:
            layer_prefix = '编组'

        if in_layer.Name == f'{layer_prefix} {in_layer.id}':
            return True

        visible = in_layer.Visible

        if in_layer.LayerType == 1:
            if in_layer.Kind == 2:
                in_layer.Name = in_layer.TextItem.Contents
            else:
                in_layer.Name = f'{layer_prefix} {in_layer.id}'
        else:
            in_layer.Name = f'{layer_prefix} {in_layer.id}'

        in_layer.Unlink()

        in_layer.AllLocked = True
        in_layer.AllLocked = False

        in_layer.Visible = visible

        return True

    def fun_所有根图层(self):
        layer_list = []
        for in_layer in self.in_doc.ArtLayers:
            res = self.fun_判断图层名字来删除广告(in_layer)
            if res is True:
                self.fun_修改图层和编组名字(in_layer)
                layer_list.append(in_layer)

        return layer_list

    def fun_所有根编组(self):
        set_list = []
        for in_layer in self.in_doc.LayerSets:
            self.fun_修改图层和编组名字(in_layer)
            set_list.append(in_layer)

        return set_list

    def fun_归递编组(self, ps_set):
        sets_list = [ps_set]
        for in_set in ps_set.LayerSets:
            self.fun_修改图层和编组名字(in_set)
            sets_list.extend(self.fun_归递编组(in_set))

        return sets_list

    def run_构建所有编组(self):
        for in_set in self.fun_所有根编组():
            self.set_list.extend(self.fun_归递编组(in_set))

    def run_构建所有图层(self):
        doc_artlayers = self.fun_所有根图层()
        self.layer_list.extend(doc_artlayers)

        for in_set in self.set_list:
            for in_layer in in_set.ArtLayers:
                res = self.fun_判断图层名字来删除广告(in_layer)

                if res is True:
                    self.fun_修改图层和编组名字(in_layer)
                    self.layer_list.append(in_layer)

    # def run_处理所有编组和图层(self):
    #     # 先列出要删除的
    #     wait_del = []
    #     for num, in_layer in enumerate(self.layer_list):
    #         res = self.fun_判断图层名字来删除广告(in_layer)
    #         if res is False:
    #             wait_del.append(num)
    #         else:
    #             self.fun_修改图层和编组名字(in_layer)
    #
    #     # 再进行列表删除
    #     for num in wait_del:
    #         self.layer_list.pop(num)
    #
    #     for in_set in self.set_list:
    #         # self.in_doc.ActiveLayer = in_set
    #         try:
    #             self.fun_修改图层和编组名字(in_set)
    #         except Exception as err:
    #             print(err)


if __name__ == '__main__':
    from win32com.client import Dispatch
    from pprint import pprint

    app = Dispatch('photoshop.application')
    app.Open(r'E:\小夕素材\9000-9999\9290\9290\小夕素材(2).psd')
    doc = app.ActiveDocument
    gal = GetAllLayer(doc)
    pprint(
        gal.layer_list
    )
