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
        self.run_处理所有编组和图层()

    @staticmethod
    def fun_判断图层名字来删除广告(in_layer):
        # 如果包含
        ad_name_include = yaml_dict.get('include_name_list')
        for ad_layer_name_single in ad_name_include:
            if in_layer.LayerType == 1:
                if in_layer.Kind != 2:
                    if ad_layer_name_single in str(in_layer.Name).lower():
                        if in_layer.AllLocked is True:
                            in_layer.AllLocked = False
                        print(f'删除图层:{in_layer.Name}')
                        in_layer.Delete()
                        return False

        # 如果等于
        ad_name_is = yaml_dict.get('is_name_list')
        if in_layer.LayerType == 1 and in_layer.Kind != 2:
            if in_layer.Name.lower() in ad_name_is:
                if in_layer.AllLocked is True:
                    in_layer.AllLocked = False
                print(f'删除图层:{in_layer.Name}')
                in_layer.Delete()
                return False

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
            layer_list.append(in_layer)
        return layer_list

    def fun_所有根编组(self):
        set_list = []
        for in_layer in self.in_doc.LayerSets:
            set_list.append(in_layer)
        return set_list

    def fun_归递编组(self, ps_set):
        sets_list = [ps_set]
        for in_set in ps_set.LayerSets:
            sets_list.extend(self.fun_归递编组(in_set))

        return sets_list

    def run_构建所有编组(self):
        for in_set in self.fun_所有根编组():
            self.set_list.extend(self.fun_归递编组(in_set))

    def run_构建所有图层(self):
        self.layer_list.extend(self.fun_所有根图层())

        for in_set in self.set_list:
            for in_layer in in_set.ArtLayers:
                self.layer_list.append(in_layer)

    def run_处理所有编组和图层(self):
        for in_set in self.set_list:
            self.fun_修改图层和编组名字(in_set)

        for in_layer in self.layer_list:
            if self.fun_判断图层名字来删除广告(in_layer) is False:
                self.layer_list.remove(in_layer)
            # else:
            #     self.fun_修改图层和编组名字(in_layer)


if __name__ == '__main__':
    from win32com.client import Dispatch

    app = Dispatch('photoshop.application')
    doc = app.ActiveDocument
    gal = GetAllLayer(doc)
    print(gal.set_list)
    print(gal.layer_list)
