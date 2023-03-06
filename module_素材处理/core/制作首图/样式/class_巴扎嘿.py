from PIL import Image

from module_素材处理.core.setting import IMG_PATH
from module_素材处理.core.图片编辑.class_picedit import PICEdit


class STBaZhaHeiStyle:
    def __init__(self, st_layout: Image.Image, title: str, material_num: str, material_format_title: str,
                 material_id: str, tb_name: str):
        self.st_layout = st_layout
        self.title = title.split(' ')
        self.material_num = material_num
        self.material_format_title = material_format_title
        self.material_id = material_id
        self.site_logo = Image.open((IMG_PATH / tb_name / 'site_logo.png').as_posix())
        self.style_bg = Image.new('RGB', (500, 1500), (0, 0, 0))

    @staticmethod
    def fun_计算边距(bg: Image.Image, past_pil: Image.Image, direction: str):
        if direction == 'x':
            return int((bg.width - past_pil.width) / 2)
        else:
            return int((bg.height - past_pil.height) / 2)

    def fun_写标题(self):
        top = 50
        padding = 50
        for title_line in self.title:
            title_line_pil = PICEdit.fun_单行文字(text=title_line, font_weight='m', font_size=220,
                                                  text_color=(255, 255, 255), bg_color=(0, 0, 0)).main()
            title_line_pil.thumbnail((500 - (padding * 2), 99999), 1)
            left = self.fun_计算边距(self.style_bg, title_line_pil, 'x')
            self.style_bg.paste(title_line_pil, (left, top))
            top += title_line_pil.height + 30
            title_line_pil.close()

    def fun_写数量和格式(self):
        top = 620
        num_pil = PICEdit.fun_单行文字(text=self.material_num + '套', font_weight='r', font_size=100,
                                       text_color=(255, 255, 255), bg_color=(0, 0, 0)).main()
        num_pil.thumbnail((400, 9999), 1)
        left = self.fun_计算边距(self.style_bg, num_pil, 'x')
        self.style_bg.paste(num_pil, (left, top))
        top += num_pil.height + 30
        num_pil.close()

        format_pil = PICEdit.fun_单行文字(text=self.material_format_title, font_weight='r', font_size=50,
                                          text_color=(255, 255, 255), bg_color=(0, 0, 0)).main()
        left = self.fun_计算边距(self.style_bg, format_pil, 'x')
        self.style_bg.paste(format_pil, (left, top))
        format_pil.close()

    def fun_贴LOGO(self):
        top = 920
        self.site_logo.thumbnail((300, 9999), 1)
        left = self.fun_计算边距(self.style_bg, self.site_logo, 'x')
        self.style_bg.paste(self.site_logo, (left, top), self.site_logo)

    def fun_写广告(self):
        top = 1240
        for line_text in ['加入会员', '全店免费']:
            line_pil = PICEdit.fun_单行文字(text=line_text, font_weight='m', font_size=100,
                                            text_color=(255, 205, 85), bg_color=(0, 0, 0)).main()
            left = self.fun_计算边距(self.style_bg, line_pil, 'x')
            self.style_bg.paste(line_pil, (left, top))
            top += line_pil.height + 20
            line_pil.close()

    def fun_写素材ID(self, bg: Image.Image):
        circle_bg = PICEdit.fun_圆角矩形背景(width=180, height=50, bg_color=(0, 0, 0))
        text_pil = PICEdit.fun_单行文字(text='ID:' + self.material_id, font_weight='m', font_size=30,
                                        text_color=(255, 255, 255), bg_color=(0, 0, 0)).main()
        left = self.fun_计算边距(circle_bg, text_pil, 'x')
        top = self.fun_计算边距(circle_bg, text_pil, 'y')
        circle_bg.paste(text_pil, (left, top))
        bg.paste(circle_bg, (30, 30), circle_bg)

        circle_bg.close()
        text_pil.close()

        return bg

    def main(self):
        self.fun_写标题()
        self.fun_写数量和格式()
        self.fun_贴LOGO()
        self.fun_写广告()

        st_bg = Image.new('RGBA', (1500, 1500), (0, 0, 0))
        st_bg.paste(self.st_layout, (0, 0))
        st_bg.paste(self.style_bg, (1000, 0))
        st_bg = self.fun_写素材ID(st_bg)

        self.st_layout.close()
        self.style_bg.close()

        return st_bg


if __name__ == '__main__':
    st_bzh = STBaZhaHeiStyle(
        st_layout=Image.new('RGBA', (1000, 1500), (199, 199, 199)),
        title='椅子 模型',
        material_num='4955',
        material_format_title='SKP草图大师素材',
        material_id='10005',
        tb_name='泡泡素材'
    )

    st_bzh.main().show()
