from core.图片编辑.fun_单行文字转PIL import TextToPIL
from core.图片编辑.fun_图片圆角 import PICToCircle
from core.图片编辑.fun_图片裁剪 import fun_图片裁剪
from core.图片编辑.fun_多行本文 import fun_多行本文
from core.图片编辑.fun_边框删除 import DelPILBorder
from core.图片编辑.fun_颜色覆盖 import fun_颜色覆盖


class PICEdit:
    fun_图片裁剪 = fun_图片裁剪
    fun_边框删除 = DelPILBorder
    fun_图片圆角 = PICToCircle
    fun_颜色覆盖 = fun_颜色覆盖
    fun_单行文字 = TextToPIL
    fun_多行本文 = fun_多行本文
