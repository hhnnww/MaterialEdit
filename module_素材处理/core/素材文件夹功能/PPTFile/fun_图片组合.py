import re
from pathlib import Path

from PIL import Image

from module_素材处理.core.图片编辑 import PICEdit


class PPTPICMerge:
    def __init__(self, pic_path: Path):
        self.pic_path = pic_path
        self.gutter = 10
        self.xq_width = 950

    def fun_所有文件(self):
        file_list = []
        for in_file in self.pic_path.iterdir():
            if in_file.is_file() and in_file.suffix.lower() in ['.png', '.jpg', '.jpeg']:
                file_list.append(in_file)

        file_list.sort(key=lambda k: self.fun_获取数字(k))
        return file_list

    @staticmethod
    def fun_获取数字(file_path: Path):
        num = re.findall(r'\d+', file_path.stem)[0]
        return int(num)

    def fun_组合图片(self):
        all_file = self.fun_所有文件()

        pic_layout = [1, 3, 3, 3, 3]
        while len(all_file) < sum(pic_layout):
            all_file += all_file

        pic_list = []
        for x in range(len(pic_layout)):
            pic_list.append([])

        num = 0
        for count, in_file in enumerate(all_file):
            pic_list[num].append(Image.open(in_file))

            if len(pic_list[num]) == pic_layout[num]:
                num += 1

            if count == sum(pic_layout) - 1:
                break

        return pic_list

    def fun_计算单排高度(self, pil_list):

        gutter_width = (len(pil_list) + 1) * self.gutter
        radio_width = sum((i.width / i.height for i in pil_list))
        oneline_height = int((self.xq_width - gutter_width) / radio_width)

        return oneline_height

    def fun_制作单排PIL(self, pil_list, oneline_height):
        bg = Image.new('RGBA', (self.xq_width, oneline_height + self.gutter), (255, 255, 255))

        x = self.gutter
        y = self.gutter
        for pil in pil_list:
            width = int(oneline_height * (pil.width / pil.height))
            img = PICEdit.fun_图片裁剪(pil, (width, oneline_height))
            img = PICEdit.fun_图片圆角(img)
            bg.paste(img, (x, y), img)
            x += img.width + self.gutter

        return bg

    def main(self):
        all_pil_list = self.fun_组合图片()
        all_line = [self.fun_制作单排PIL(pil, self.fun_计算单排高度(pil)) for pil in all_pil_list]
        height = sum(
            (line.height for line in all_line)
        ) + self.gutter
        bg = Image.new('RGBA', (self.xq_width, height), (255, 255, 255))
        x = 0
        y = 0
        for line in all_line:
            bg.paste(line, (x, y), line)
            y += line.height

        return bg


if __name__ == '__main__':
    PPTPICMerge(
        Path(r'X:\H000-H999\H0257\H0257\小夕素材(1)')
    ).main().show()
