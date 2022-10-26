def fun_归递编组(group_item):
    """
    传递进来一个编组，进行归递
    :param group_item: 编组
    :return:
    """
    item_list = [group_item]
    if group_item.GroupItems.Count > 0:

        for in_item in group_item.GroupItems:
            item_list.extend(fun_归递编组(in_item))

    return item_list


def fun_获取图层下的所有编组(in_layer):
    """
    传进来一个广告图层，遍历图层下所有的编组
    :param in_layer: 广告图层
    :return:
    """
    group_list = []
    if in_layer.GroupItems.Count > 0:
        for item in in_layer.GroupItems:
            group_list.append(item)

            if item.GroupItems.Count > 0:
                for in_item in item.GroupItems:
                    group_list.append(in_item)

                    if in_item.GroupItems.Count > 0:
                        for in_in_item in in_item.GroupItems:
                            group_list.append(in_in_item)

    return group_list


def fun_获取图层下所有路径(in_layer):
    """
    传进来广告图层，获取广告图层下所有路径
    :param in_layer:
    :return:
    """
    path_list = []

    if in_layer.PathItems.Count > 0:
        for path_item in in_layer.PathItems:
            path_list.append(path_item)

    for group_item in fun_获取图层下的所有编组(in_layer):
        if group_item.PathItems.Count > 0:
            for path_item in group_item.PathItems:
                path_list.append(path_item)

    return path_list
