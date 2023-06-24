from pathlib import Path
from time import sleep

from win32com.client import Dispatch


class AIFile:
    def __init__(self, file: Path, tb_name: str):
        print('\n处理AI文件：', file.as_posix(), '\n')
        self.file = file
        self.tb_name = tb_name

        self.app = Dispatch('Illustrator.Application')
        try:
            self.app.Open(file.as_posix())
        except Exception as err:
            print(err)
            self.app.Quit()
            sleep(5)
            self.app.Open(file.as_posix())

        self.doc = self.app.ActiveDocument

    def fun_删除afd广告(self):
        ad_layer = list(self.doc.Layers)[-1]

        for item in ad_layer.GroupItems:
            if 70 < item.Height < 80:
                if (float(item.Height) + abs(float(item.Top))) - float(self.doc.Height) < 10:
                    if abs(int(item.Left)) == 0:
                        print('success')
                        item.Locked = False
                        item.Delete()

    def fun_根据图层名字删除广告(self):
        ad_layer_name_list = ['小夕素材', '火山素材=9.9全店免费', '火山素材https://shop185838729.taobao.com/']
        layer_list = []
        for layer in self.doc.Layers:
            layer_list.append(layer)

        for layer in layer_list:
            layer_status = True

            if layer.Name in ad_layer_name_list:
                if layer.Locked is True:
                    layer.Locked = False

                print(f'删除图层：\t{layer.Name}')
                layer.Delete()
                layer_status = False

            if layer_status is True:
                if '火山素材' in layer.Name:
                    layer.Name = layer.Name.replace('火山', '小夕')

    def fun_添加自己的文字(self):
        # 添加文字图层
        new_layer = self.doc.Layers.Add()

        # 初始化文字框
        new_layer.Name = self.tb_name
        text_frame = self.doc.PathItems.Rectangle(0, 0, int(self.doc.Width), int(self.doc.Height))

        # 放内容
        area_text_ref = self.doc.TextFrames.AreaText(text_frame)

        if self.tb_name == '小夕素材':
            area_text_ref.Contents = "淘宝店铺：小夕素材\nxiaoxisc.com\n购买时请认准官方店铺。"
        elif self.tb_name == '饭桶设计':
            area_text_ref.Contents = "淘宝店铺：饭桶设计\nfantongdesign.com\n购买时请认准官方店铺。"

        for art_frame in new_layer.TextFrames:
            for art_range in art_frame.Characters:
                attr = art_range.CharacterAttributes

                # 设置字体
                attr.TextFont = self.app.TextFonts.GetFontByName('OPPOSans-M')

                # attr.FillColor.Blue = 0
                # attr.FillColor.Green = 0
                # attr.FillColor.Red = 0

                attr.Size = 24

        new_layer.Locked = True

    def fun_导出PNG(self):
        if list(self.doc.Layers)[0].Name == self.tb_name:
            list(self.doc.Layers)[0].Visible = False

        png_path = self.file.with_suffix('.png')
        radio = int(4000 / max((
            int(self.doc.Width), int(self.doc.Height)
        ))) * 100

        eo = Dispatch("Illustrator.ExportOptionsPNG24")
        eo.HorizontalScale = radio
        eo.VerticalScale = radio
        eo.ArtBoardClipping = True

        self.doc.Export(png_path.as_posix(), 5, eo)

        if list(self.doc.Layers)[0].Name == self.tb_name:
            list(self.doc.Layers)[0].Visible = True

    def main(self):
        board_one = self.doc.Artboards[0]
        board_one.Name = self.file.stem

        # self.fun_删除afd广告()

        self.fun_根据图层名字删除广告()
        self.fun_导出PNG()

        if list(self.doc.Layers)[0].Name != self.tb_name:
            self.fun_添加自己的文字()

        self.file.unlink()
        new_file = self.file.with_suffix('.ai')

        self.doc.SaveAs(new_file.as_posix())
        self.doc.Close(2)
        sleep(2)


if __name__ == '__main__':
    AIFile(
        file=Path(r'F:\小夕素材\10000-10999\10069\10069\小夕素材(3).ai'),
        tb_name='小夕素材'
    ).main()
