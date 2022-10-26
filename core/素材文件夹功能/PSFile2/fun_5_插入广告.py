from pathlib import Path

from win32com.client import Dispatch


def fun_插入广告(app, doc, tb_name: str, ad_layer_name: str):
    if doc.ArtLayers.Count > 0:
        if doc.ArtLayers.Item(1).Name == ad_layer_name:
            return

    doc.ArtLayers.Add()

    tb_ad_png = Path(__file__).parent.parent.parent / 'IMG' / f'{tb_name}' / '二维码.png'
    desc = Dispatch('Photoshop.ActionDescriptor')
    desc.PutPath(app.CharIDToTypeID('null'), tb_ad_png)
    app.ExecuteAction(app.CharIDToTypeID('Plc '), desc)

    if doc.ArtLayers.Count > 0:
        doc.ArtLayers.Item(1).Name = ad_layer_name
