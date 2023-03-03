from module_素材处理.core.素材文件夹功能.PSFile2.open_yaml import open_yml


def fun_文字图层替换内容(item):
    visible = item.Visible
    item.AllLocked = False

    keywords = open_yml().get('ad_replace_keywords')

    for key in keywords:
        if key[0].lower() in str(item.textItem.Contents).lower():

            if 'bold' in str(item.textItem.Font).lower():
                item.TextItem.Font = "Alibaba_PuHuiTi_2_85_Bold"
            else:
                item.TextItem.Font = "Alibaba_PuHuiTi_2_55_Regular"

            item.TextItem.Contents = item.TextItem.Contents.replace(key[0], key[1])
            item.Name = item.TextItem.Contents

    item.Visible = visible
