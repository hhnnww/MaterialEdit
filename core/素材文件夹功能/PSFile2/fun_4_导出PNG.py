from pathlib import Path

from win32com.client import Dispatch


def export_png(ref_doc, file: Path, ad_layer_name: str, del_ad_layer: bool = False):
    """
    导出PNG图片
    可以选择是否删除自己的广告

    :param ref_doc: 当前PS打开的文档
    :param file: PSD文件路径
    :param ad_layer_name: 自己店铺的广告名字
    :param del_ad_layer: 是否删除自己店铺的广告
    :return:
    """
    png_path = file.with_suffix('.png')

    if ref_doc.ArtLayers.Count > 0:
        # 第一个广告图层
        ad_layer = ref_doc.ArtLayers.Item(1)

        if ad_layer.Name in [ad_layer_name, '隐藏 或 删除此图层即可开始您的编辑.',
                             '隐藏 或 删除此图层即可开始您的编辑.']:

            if del_ad_layer is True:
                ad_layer.AllLocked = False
                ad_layer.Delete()
            else:
                ad_layer.Visible = False

    export_option = Dispatch('Photoshop.ExportOptionsSaveForWeb')
    export_option.Format = 13
    export_option.PNG8 = False
    export_option.Dither = 2
    ref_doc.Export(png_path.as_posix(), 2, export_option)

    if ref_doc.ArtLayers.Count > 0:
        ad_layer = ref_doc.ArtLayers.Item(1)
        if del_ad_layer is False:
            if ad_layer.Name == ad_layer_name:
                ad_layer.Visible = True

    return png_path
