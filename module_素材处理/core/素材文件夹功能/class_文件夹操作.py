from module_素材处理.core.素材文件夹功能.PPTFile import PPTEdit
from module_素材处理.core.素材文件夹功能.PSFile2.class_PSFile import PSFile
from module_素材处理.core.素材文件夹功能.PSFile2.fun_2_导出所有图层 import fun_清空OUT_PATH
from module_素材处理.core.素材文件夹功能.PSFile2.fun_3_对比所有图片 import fun_所有广告图片
from module_素材处理.core.素材文件夹功能.fun_AI_文件处理2 import AIFile
from module_素材处理.core.素材文件夹功能.fun_指定遍历 import fun_指定遍历
from module_素材处理.core.素材文件夹功能.fun_文件重命名 import MaterialFolderRename
from module_素材处理.core.素材文件夹功能.fun_移动到根目录 import fun_移动到根目录
from module_素材处理.core.素材文件夹功能.fun_移动图片 import fun_复制图片到指定目录
from module_素材处理.core.素材文件夹功能.fun_解压ZIP import fun_解压ZIP
from .FontToPng2.class_font_to_png import FontToPng
from .fun_享设计文件夹重命名 import XiangDesignPathRename
# from .FontToPIL.fun_字体生成图片 import FontToPIL
from .fun_删除相同文件 import DelSameFile
from .fun_制作文件夹预览 import MakePathPreviewImage
from .fun_压缩为rar import fun_压缩为RAR
from .fun_按数字分类 import CateByNum
from .fun_按格式分类 import CateBySuffix
from .fun_生成SKP批量导出 import fun_生成SKP批量导出脚本
from .fun_素材图蜘蛛水印 import fun_素材图蜘蛛水印
from .fun_重命名字体文件 import FontPathReName
from module_素材处理.core.素材文件夹功能.PSFile3.class_PSFile import PSFile as PS3File


class MaterialFolderFunction:
    fun_移动到根目录 = fun_移动到根目录
    fun_文件重命名 = MaterialFolderRename
    fun_指定遍历 = fun_指定遍历
    fun_复制图片到指定目录 = fun_复制图片到指定目录
    fun_解压ZIP = fun_解压ZIP
    fun_PS操作 = PSFile
    fun_PS广告图片 = fun_所有广告图片
    fun_PPT操作 = PPTEdit
    fun_AI操作 = AIFile
    fun_清空OUT_PATH = fun_清空OUT_PATH
    fun_删除相同文件 = DelSameFile
    fun_字体重命名 = FontPathReName
    fun_按格式分类 = CateBySuffix
    fun_字体生成图片 = FontToPng
    fun_按数字分类 = CateByNum
    fun_压缩为RAR = fun_压缩为RAR
    fun_生成SKP批量导出脚本 = fun_生成SKP批量导出脚本
    fun_素材图蜘蛛水印 = fun_素材图蜘蛛水印
    fun_制作文件夹预览 = MakePathPreviewImage
    fun_享设计文件夹改名 = XiangDesignPathRename
    fun_PS3操作 = PS3File
