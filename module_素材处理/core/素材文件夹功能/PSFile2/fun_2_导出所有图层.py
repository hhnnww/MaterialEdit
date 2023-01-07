import shutil
from pathlib import Path

from win32com.client import Dispatch

from module_素材处理.core.setting import OUT_PATH
from module_素材处理.core.素材文件夹功能.PSFile2.fun_1_遍历所有图层 import run_所有图层
from module_素材处理.core.素材文件夹功能.PSFile2.fun_PS基础操作 import dialog
from module_素材处理.core.素材文件夹功能.PSFile2.fun_PS基础操作 import s


def fun_清空OUT_PATH():
    for in_file in OUT_PATH.iterdir():
        if in_file.is_file():
            in_file.unlink()

        else:
            shutil.rmtree(in_file)


def fun_导出单个图层(in_layer, file: Path):
    in_out_path = OUT_PATH / file.stem.lower()
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
    if item.Kind not in [1, 17]:
        return False

    # 混合模式如果不是正常
    if item.BlendMode != 2:
        return False

    # 透明度如果不是100%
    if int(item.FillOpacity) < 100:
        return False

    # 如果是印盖图层
    if item.Grouped is True:
        return False

    # 如果在文档之外
    l, t, r, b = item.Bounds
    if r <= 0 or b <= 0 or l >= doc_bounds[0] or t >= doc_bounds[1]:
        return False

    # 如果大于宽高三分之一
    # if int(abs(r - l)) > int(doc_bounds[0] / 3) or int(abs(b - t)) > int(doc_bounds[1] / 3):
    #     return False

    # 如果是隐藏图层
    if item.Visible is False:
        return False

    return True


def run_导出所有图层(in_doc, file: Path, ad_name: str):
    # fun_清空OUT_PATH()
    all_item = run_所有图层(in_doc, ad_name)
    art_layer_item_list = []
    text_item_list = []
    for item in all_item:
        print(f'导出图层:{item.Name}')
        if item.Bounds == (0.0, 0.0, 0.0, 0.0):
            if item.AllLocked is True:
                item.AllLocked = False

            item.Delete()

        elif is_export_layer(item, (in_doc.Width, in_doc.Height)) is True:
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


__all__ = ['run_导出所有图层', 'fun_清空OUT_PATH']
