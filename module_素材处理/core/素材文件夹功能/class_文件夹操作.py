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
from .fun_删除相同文件 import DelSameFile


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
