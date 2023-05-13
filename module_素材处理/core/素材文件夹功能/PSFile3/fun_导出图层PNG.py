import shutil
from pathlib import Path
from typing import Any
from typing import List

from pydantic import BaseModel
from win32com.client import CDispatch
from win32com.client import Dispatch

from module_素材处理.core.setting import OUT_PATH
from module_素材处理.core.素材文件夹功能.PSFile3.fun_PS基础操作 import dialog
from module_素材处理.core.素材文件夹功能.PSFile3.fun_PS基础操作 import s


def fun_清空OUT_PATH():
    """
    清空桌面OUT_PATH文件夹
    :return:
    """
    for in_file in OUT_PATH.iterdir():
        if in_file.is_file():
            in_file.unlink()

        else:
            shutil.rmtree(in_file)


def fun_导出单个图层(app: CDispatch, in_layer: CDispatch, file: Path, ref_doc: CDispatch) -> Path:
    """
    传入单个图层，并且导出到桌面PNG
    :param app:
    :param in_layer:
    :param file: PS文件
    :param ref_doc:
    :return:
    """
    in_out_path = OUT_PATH / file.stem.lower()

    if in_out_path.exists() is False:
        in_out_path.mkdir(parents=True)

    ref_doc.ActiveLayer = in_layer

    # 导出图片
    desc = Dispatch("Photoshop.ActionDescriptor")
    ref = Dispatch("Photoshop.ActionReference")
    ref.PutEnumerated(s(app, "layer"), s(app, "ordinal"), s(app, "targetEnum"))
    desc.PutReference(s(app, "null"), ref)
    desc.PutString(s(app, "fileType"), "png")
    desc.PutInteger(s(app, "quality"), 32)
    desc.PutInteger(s(app, "metadata"), 0)

    desc.PutString(s(app, "destFolder"), in_out_path.as_posix())
    desc.PutBoolean(s(app, "sRGB"), True)
    desc.PutBoolean(s(app, "openWindow"), True)
    app.ExecuteAction(s(app, "exportSelectionAsFileTypePressed"), desc, dialog())

    img_path = in_out_path / (in_layer.Name + '.png')

    return img_path


def fun_比例判断(item: CDispatch, ad_list):
    """
    先判断图层的比例，然后判断图片列表的图片比例
    如果相同则导出
    :param item:
    :param ad_list:
    :return:
    """
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
    """

    :param item:
    :param doc_bounds:
    :return:
    """
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
    # if item.BlendMode != 2:
    #     return False

    # 透明度如果不是100%
    # if int(item.FillOpacity) < 100:
    #     return False

    # 如果是印盖图层
    if item.Grouped is True:
        return False

    # 如果在文档之外
    l, t, r, b = item.Bounds
    if r <= 0 or b <= 0 or l >= doc_bounds[0] or t >= doc_bounds[1] \
            or l <= 0 or r >= doc_bounds[0] or t <= 0 or b >= doc_bounds[1]:
        return False

    # 如果大于宽高三分之一
    if int(abs(r - l)) > int(doc_bounds[0] / 3) or int(abs(b - t)) > int(doc_bounds[1] / 3):
        return False

    # 如果是隐藏图层
    # if item.Visible is False:
    #     return False

    return True


class LayerItem(BaseModel):
    item: Any
    img_path: Path


def run_导出所有图层(app: CDispatch, in_doc: CDispatch, file: Path, layer_list: List[CDispatch]) -> List[LayerItem]:
    export_layer_list = []

    # fun_清空OUT_PATH()
    for item in layer_list:

        if item.Kind != 2:
            if item.Bounds == (0.0, 0.0, 0.0, 0.0):
                item.Delete()

            elif is_export_layer(item, (in_doc.Width, in_doc.Height)) is True:
                try:
                    img_path = fun_导出单个图层(app, item, file, in_doc)
                except:
                    pass
                else:
                    export_layer_list.append(
                        LayerItem(
                            item=item,
                            img_path=img_path
                        )
                    )

    return export_layer_list
