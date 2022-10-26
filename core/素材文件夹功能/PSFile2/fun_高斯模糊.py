from core.素材文件夹.PSFile2.fun_PS基础操作 import *


def gaussianBlur_0(app):
    desc234 = Dispatch("Photoshop.ActionDescriptor")
    desc234.PutUnitDouble(s("radius"), s("pixelsUnit"), 50.000000)
    app.ExecuteAction(s("gaussianBlur"), desc234, dialog())
