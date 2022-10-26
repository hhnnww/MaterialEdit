import shutil
from pathlib import Path

from win32com.client import Dispatch

from core.setting import out_path
from core.素材文件夹.PSFile2.fun_1_遍历所有图层 import run_所有图层
from core.素材文件夹.PSFile2.fun_PS基础操作 import s, dialog


def fun_清空OUT_PATH():
    for in_file in out_path.iterdir():
        if in_file.is_file():
            in_file.unlink()

        else:
            shutil.rmtree(in_file)


def fun_导出单个图层(in_layer, file: Path):
    in_out_path = out_path / file.stem.lower()
    if in_out_path.exists() is False:
        in_out_path.mkdir(parents=True)

    # 导出单个图层
    app = Dispatch("Photoshop.Application")

    # 选择图层
    desc284 = Dispatch("Photoshop.ActionDescriptor")
    ref12 = Dispatch("Photoshop.ActionReference")
    list8 = Dispatch("Photoshop.ActionList")
    ref12.PutName(s("layer"), in_layer.Name)
    desc284.PutReference(s("target"), ref12)
    desc284.PutBoolean(s("makeVisible"), False)
    list8.PutInteger(in_layer.id)
    desc284.PutList(s("layerID"), list8)
    app.ExecuteAction(s("select"), desc284, dialog())

    # 导出图片
    desc = Dispatch("Photoshop.ActionDescriptor")
    ref = Dispatch("Photoshop.ActionReference")
    ref.PutEnumerated(s("layer"), s("ordinal"), s("targetEnum"))
    desc.PutReference(s("null"), ref)
    desc.PutString(s("fileType"), "png")
    desc.PutInteger(s("quality"), 32)
    desc.PutInteger(s("metadata"), 0)

    desc.PutString(s("destFolder"), in_out_path.as_posix())
    desc.PutBoolean(s("sRGB"), True)
    desc.PutBoolean(s("openWindow"), True)
    app.ExecuteAction(s("exportSelectionAsFileTypePressed"), desc, dialog())

    img_path = in_out_path / (in_layer.Name + '.png')

    return img_path


def fun_比例判断(item, ad_list):
    bounds = item.Bounds
    item_width = bounds[2] - bounds[0]
    item_height = bounds[3] - bounds[1]
    ratio = item_height / item_width

    for ad_pic in ad_list:
        ad_ratio = ad_pic.shape[0] / ad_pic.shape[1]
        if abs(ad_ratio - ratio) < 0.1:
            return True

    return False


def fun_文档比例(item, doc_bounds):
    bounds = item.Bounds
    item_width = bounds[2] - bounds[0]
    item_height = bounds[3] - bounds[1]
    ratio = item_height / item_width

    if abs(ratio - (doc_bounds[1] / doc_bounds[0])) < 0.1:
        return True

    return False


def fun_两个数字中间(num, a, b):
    if a < num < b:
        return True

    return False


def is_export_layer(item, doc_bounds):
    bounds = item.Bounds
    item_width = bounds[2] - bounds[0]
    item_height = bounds[3] - bounds[1]

    if item.Grouped is True:
        return False

    if item.Visible is False:
        return False

    if item_width > doc_bounds[0] or item_height > doc_bounds[1]:
        return False

    # 起点不在文档中间
    if fun_两个数字中间(bounds[0], 0, doc_bounds[0]) is False or fun_两个数字中间(bounds[1], 0, doc_bounds[1]) is False:
        return False

    # 终点不在文档中间
    if fun_两个数字中间(bounds[2], 0, doc_bounds[0]) is False or fun_两个数字中间(bounds[3], 0,
                                                                                  doc_bounds[1]) is False:
        return False

    if item.Kind in [1, 17]:
        return True

    return False


def run_导出所有图层(in_doc, file: Path):
    # fun_清空OUT_PATH()

    all_item = run_所有图层(in_doc)
    art_layer_item_list = []
    text_item_list = []
    for item in all_item:
        if item.Bounds == (0.0, 0.0, 0.0, 0.0):
            if item.AllLocked is True:
                item.AllLocked = False

            item.Delete()

        elif is_export_layer(item, (in_doc.Width, in_doc.Height)) is True:
            print(item.Name)
            img_path = fun_导出单个图层(item, file)
            art_layer_item_list.append(
                dict(
                    item=item,
                    img_path=img_path
                )
            )

        elif item.Kind == 2:
            text_item_list.append(item)

    return art_layer_item_list, text_item_list


__all__ = ['run_导出所有图层']
