from PIL import Image

from module_素材处理.core.setting import IMG_PATH
from module_素材处理.core.制作首图.样式.class_T500标题 import fun_T500标题
from module_素材处理.core.图片编辑 import PICEdit


class STT500:
    def __init__(self, st: Image.Image, title: str, sc_id: str, tb_name: str, type_title: str):
        self.st = st
        self.title = title
        self.sc_id = sc_id
        self.tb_name = tb_name
        self.type_title = type_title

    def make_type_pil(self):
        """
        制作 大标题下面的小标题
        """
        text_pil = PICEdit.fun_单行文字(self.type_title, font_size=30, font_weight='b', text_color=(255, 205, 85),
                                        bg_color=(0, 0, 0), font_family='oppo').main()
        bg = PICEdit.fun_圆角矩形背景(345, 58, (0, 0, 0))
        bg.paste(text_pil, (
            int((bg.width - text_pil.width) / 2),
            int((bg.height - text_pil.height) / 2)
        ))
        gutter = 20

        ad_text_pil = PICEdit.fun_单行文字(
            '全元素可编辑 全自动秒发货', font_size=35, font_weight='b', text_color=(0, 0, 0), bg_color=(255, 205, 85),
            font_family='oppo'
        ).main()
        new_bg = Image.new('RGB', (bg.width + ad_text_pil.width + gutter, max(bg.height, ad_text_pil.height + 40)),
                           (255, 205, 85))
        new_bg.paste(bg, (0, int((new_bg.height - bg.height) / 2)), bg)
        new_bg.paste(ad_text_pil, (gutter + bg.width, int((new_bg.height - ad_text_pil.height) / 2)))

        return new_bg

    def make_title_pil(self):
        """
        制作大标题
        顺便把小标题粘贴进去
        """
        type_pil = self.make_type_pil()
        bg = Image.new('RGBA', (960, 240), (255, 255, 255, 0))
        circle = PICEdit.fun_圆角矩形背景(960, 240, (255, 205, 85))
        bg.paste(circle, (0, 0), circle)

        title_pil = fun_T500标题(self.title)
        title_pil.thumbnail((790, 100))

        bg.paste(title_pil, (
            int((bg.width - title_pil.width) / 2),
            int((bg.height - type_pil.height - title_pil.height + 10) / 2)
        ))
        bg.paste(type_pil, (
            int((bg.width - type_pil.width) / 2),
            int(bg.height - type_pil.height) - 10
        ))

        return bg

    def make_circle(self):
        """
        制作圆圈 上面贴LOGO 下面贴货号
        顺便把上面的大标题粘贴上来
        """
        bg = PICEdit.fun_圆角矩形背景(550, 550, (0, 0, 0))

        title_pil = self.make_title_pil()

        logo = Image.open(IMG_PATH / self.tb_name / 'site_logo.png')
        logo.thumbnail((
            bg.width, int(((bg.height - 80 - title_pil.height) / 2) - 10)
        ))
        for x in range(logo.width):
            for y in range(logo.height):
                r, g, b, a = logo.getpixel((x, y))
                bg_color = (255, 205, 85, a)
                logo.putpixel((x, y), bg_color)

        bg.paste(logo, (
            int((bg.width - logo.width) / 2),
            int((((bg.height - title_pil.height) / 2) - logo.height) / 2) + 5
        ), logo)

        # 圆形下方的 广告语 货号
        ad_pil = PICEdit.fun_单行文字(f'{self.tb_name} 只卖精品', font_size=30, font_weight='b',
                                      text_color=(255, 205, 85),
                                      bg_color=(0, 0, 0), font_family='oppo').main()
        sc_id_pil = PICEdit.fun_单行文字(f'ID:{self.sc_id}', font_size=26, font_weight='b', text_color=(255, 205, 85),
                                         bg_color=(0, 0, 0), font_family='oppo').main()

        bottom_height = int((bg.height - title_pil.height) / 2)
        top = bottom_height + title_pil.height + ((bottom_height - ad_pil.height - sc_id_pil.height - 20) / 2)
        top = int(top) - 5

        bg.paste(ad_pil, (int((bg.width - ad_pil.width) / 2), top))
        top += ad_pil.height + 20
        bg.paste(sc_id_pil, (int((bg.width - sc_id_pil.width) / 2), top))

        # 把标题粘贴进来
        new_bg = Image.new('RGBA', (
            title_pil.width, bg.height
        ), (255, 255, 255, 0))

        new_bg.paste(bg, (
            int((new_bg.width - bg.width) / 2), 0
        ), bg)
        new_bg.paste(
            title_pil, (0, int((new_bg.height - title_pil.height) / 2)), title_pil
        )
        return new_bg

    def main(self):
        """
        先粘贴首图，然后把上面circle包含了标题的
        粘贴到首图上面
        """
        main_pil = self.make_circle()
        self.st.paste(main_pil, (
            int((self.st.width - main_pil.width) / 2), int((self.st.height - main_pil.height) / 2)
        ), main_pil)
        return self.st


if __name__ == '__main__':
    t = STT500(
        st=Image.new('RGB', (1500, 1500), (255, 255, 255)),
        title='16套 中秋节节日海报',
        sc_id='6001',
        tb_name='小夕素材',
        type_title='AI矢量设计素材'
    )

    t.main().show()
