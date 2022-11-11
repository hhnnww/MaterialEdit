from module_素材处理.core.图片编辑.fun_单行文字转PIL import TextToPIL
from module_素材处理.core.图片编辑.fun_图片圆角 import PICToCircle
from module_素材处理.core.图片编辑.fun_图片裁剪 import fun_图片裁剪
from module_素材处理.core.图片编辑.fun_圆角矩形背景 import fun_圆角矩形背景
from module_素材处理.core.图片编辑.fun_多行本文 import fun_多行本文
from module_素材处理.core.图片编辑.fun_边框删除 import DelPILBorder
from module_素材处理.core.图片编辑.fun_颜色覆盖 import fun_颜色覆盖
from .fun_调整图片不透明度 import fun_图片添加不透明度
from .class_字体文件生成图片 import FontToPIL


class PICEdit:
    fun_图片裁剪 = fun_图片裁剪
    fun_边框删除 = DelPILBorder
    fun_图片圆角 = PICToCircle
    fun_颜色覆盖 = fun_颜色覆盖
    fun_单行文字 = TextToPIL
    fun_多行本文 = fun_多行本文
    fun_圆角矩形背景 = fun_圆角矩形背景
    fun_图片添加不透明度 = fun_图片添加不透明度
    fun_字体文件生成图片 = FontToPIL
