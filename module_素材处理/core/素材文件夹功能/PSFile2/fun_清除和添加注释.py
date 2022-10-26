from win32com.client import Dispatch


def fun_清理注释(app):
    def s(name):
        return app.StringIDToTypeID(f"{name}")

    def ps_display_dialogs():
        return {"all": 1, "error": 2, "no": 3}

    def dialog(dialog_type="no"):
        dialogs = ps_display_dialogs()
        return dialogs.get(dialog_type, lambda: None)

    desc364 = Dispatch('Photoshop.ActionDescriptor')
    app.ExecuteAction(app.StringIDToTypeID("deleteAllAnnot"), desc364, 2)

    def make_0():
        desc309 = Dispatch("Photoshop.ActionDescriptor")
        ref9 = Dispatch("Photoshop.ActionReference")
        desc310 = Dispatch("Photoshop.ActionDescriptor")
        desc311 = Dispatch("Photoshop.ActionDescriptor")
        desc312 = Dispatch("Photoshop.ActionDescriptor")
        ref9.PutClass(s("annotation"))
        desc309.PutReference(s("target"), ref9)
        desc311.PutUnitDouble(s("horizontal"), s("pixelsUnit"), -1036.849072)
        desc311.PutUnitDouble(s("vertical"), s("pixelsUnit"), 684.000000)
        desc310.PutObject(s("location"), s("paint"), desc311)
        desc312.PutUnitDouble(s("horizontal"), s("pixelsUnit"), 240.000000)
        desc312.PutUnitDouble(s("vertical"), s("pixelsUnit"), 140.000000)
        desc310.PutObject(s("size"), s("offset"), desc312)
        desc310.PutEnumerated(s("annotType"), s("annotType"), s("annotText"))
        desc309.PutObject(s("using"), s("annotation"), desc310)
        app.ExecuteAction(s("make"), desc309, dialog())

    make_0()

    def set_1():
        desc314 = Dispatch("Photoshop.ActionDescriptor")
        ref10 = Dispatch("Photoshop.ActionReference")
        desc315 = Dispatch("Photoshop.ActionDescriptor")
        ref10.PutIndex(s("annotation"), 0)
        desc314.PutReference(s("target"), ref10)
        desc315.PutString(s("text"),
                          """网址：xiaoxisc.com\n\n\n同行请勿搬运，否则投诉到底。\n\n\n严重会导致巨额赔偿，并封店。""")
        desc314.PutObject(s("to"), s("annotation"), desc315)
        app.ExecuteAction(s("set"), desc314, dialog())

    set_1()
