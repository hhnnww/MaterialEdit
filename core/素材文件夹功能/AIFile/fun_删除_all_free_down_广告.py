from core.素材文件夹.AIFile.fun_获取图层下所有编组 import fun_获取图层下的所有编组, fun_获取图层下所有路径


def fun_删除_all_free_down_广告(doc):
    count = doc.Layers.Count
    ad_layer = doc.Layers.Item(count)

    # 删除广告背景
    bg_height = fun_删除广告背景(doc=doc, ad_layer=ad_layer)

    # 删除文字
    group_list = fun_获取图层下的所有编组(ad_layer)
    for group_item in group_list:
        if fun_删除广告文字编组_31(group_item=group_item) is True or fun_删除广告文字编组_2(
                group_item=group_item) is True:
            group_item.Delete()

    # 背景图层裁剪
    print('裁剪背景')
    fun_裁剪背景(ad_layer=ad_layer, height=bg_height)

    # 画板裁剪
    print('裁剪画板')
    fun_裁剪画板(doc=doc, height=bg_height)


def fun_获取颜色(path_item):
    color = (
        int(path_item.FillColor.Red),
        int(path_item.FillColor.Green),
        int(path_item.FillColor.Blue)
    )
    return color


def fun_判断颜色(group_item):
    for path_item in group_item.PathItems:
        color = fun_获取颜色(path_item=path_item)
        if color not in [(0, 0, 0), (255, 255, 255)]:
            return False

    return True


def fun_删除广告文字编组_31(group_item):
    if group_item.GroupItems.Count == 0 and group_item.PathItems.Count == 17 and group_item.PageItems.Count == 31:
        if fun_判断颜色(group_item=group_item) is True:
            return True
    return False


def fun_删除广告文字编组_2(group_item):
    # TODO: 判断颜色
    if group_item.GroupItems.Count == 2 and group_item.PathItems.Count == 0 and group_item.PageItems.Count == 2:
        first_group = group_item.GroupItems.Item(1)
        sec_group = group_item.GroupItems.Item(2)
        if first_group.GroupItems.Count == 2 and sec_group.PageItems.Count == 29:
            return True

    return False


def fun_删除广告背景(doc, ad_layer):
    path_list = fun_获取图层下所有路径(ad_layer)
    for path_item in path_list:
        if int(path_item.Width) == int(doc.Width):
            color = (
                int(path_item.FillColor.Red), int(path_item.FillColor.Green), int(
                    path_item.FillColor.Blue)
            )
            if color in [(19, 32, 40), ]:
                bg_height = path_item.Height
                print(f'删除背景路径 uuid:{path_item.Uuid}')
                path_item.Delete()

                return bg_height

    return 70


def fun_裁剪背景(ad_layer, height):
    count = ad_layer.PathItems.Count
    bg_path = ad_layer.PathItems.Item(count)
    bg_path.Height = bg_path.Height - height


def fun_裁剪画板(doc, height):
    bord = doc.Artboards.Item(1)
    bord_area = list(bord.ArtboardRect)
    bord_area[3] = bord_area[3] + height
    bord.ArtboardRect = tuple(bord_area)
