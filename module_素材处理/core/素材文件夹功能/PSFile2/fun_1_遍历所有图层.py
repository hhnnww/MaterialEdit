def fun_修改图层和编组名(in_layer):
    ad_layer_name_list = [
        '隐藏 或 删除此图层即可开始您的编辑.',
        'sy',
        '摄图网二维码',
        'sttttt',
        '摄图网水印',
        '千图小程序',
        'logo',
        '微信图片_20220602162527',
    ]
    if in_layer.Name.lower() in ad_layer_name_list:
        if in_layer.AllLocked is True:
            in_layer.AllLocked = False

        in_layer.Delete()
        return False

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

    in_layer.Unlink()

    in_layer.AllLocked = True
    in_layer.AllLocked = False

    in_layer.Visible = visible

    return True


def fun_归递编组(layerset):
    """
    归递一个编组下的所有编组
    :param layerset:
    :return:
    """
    layerset_list = [layerset]

    # 修改编组名称
    fun_修改图层和编组名(layerset)

    try:
        (layerset.LayerSets.Count > 0) is True
    except:
        pass
    else:
        for in_layerset in layerset.LayerSets:
            layerset_list.extend(fun_归递编组(in_layerset))

    return layerset_list


def run_所有编组(in_doc):
    """
    遍历文档下的所有编组
    然后把所有编组合并到一个列表中
    :param in_doc:
    :return:
    """
    layerset_list = []
    try:
        (in_doc.LayerSets.Count > 0) is True
    except:
        pass
    else:
        for in_layerset in in_doc.LayerSets:
            layerset_list.extend(fun_归递编组(in_layerset))

    return layerset_list


def fun_根图层(in_doc):
    """
    获取文档下的所有根图层
    :param in_doc:
    :return:
    """
    artlayers_list = []
    if in_doc.ArtLayers.Count > 0:
        for in_art_layer in in_doc.ArtLayers:
            if fun_修改图层和编组名(in_art_layer) is True:
                artlayers_list.append(in_art_layer)

    return artlayers_list


def run_所有图层(in_doc):
    """
    先获取根图层
    然后遍历所有编组，把所有编组都合并到列表中
    """
    art_layers_list = []
    art_layers_list.extend(fun_根图层(in_doc))

    for layerset in run_所有编组(in_doc):
        try:
            (layerset.ArtLayers.Count > 0) is True
        except:
            pass
        else:
            for in_art_layer in layerset.ArtLayers:
                if fun_修改图层和编组名(in_art_layer) is True:
                    art_layers_list.append(in_art_layer)

    return art_layers_list


__all__ = ['run_所有图层']
