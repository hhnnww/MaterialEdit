import re
from pathlib import Path
from typing import Optional, List

from PIL import Image
from fastapi import APIRouter

router = APIRouter(prefix='/图片自动拼图')


# --------------- 图片粘贴到一起 ---------------

class AutoMergeImage:
    direction: str = 'y'
    folder: Optional[Path] = None
    gutter: int = 0
    pic_list: Optional[List[str]] = None

    @classmethod
    def open_path(cls, folder: str, pic_list: List[str]):
        cls.folder = Path(folder)
        cls.pic_list = pic_list
        return cls()

    @staticmethod
    def get_stem(in_file: Path) -> int:
        """
        获取stem中的数字，如果没有数字
        返回 0
        :param in_file:
        :return:
        """
        num = re.findall(r'\d+', in_file.stem)[0]
        if len(num) > 0:
            return int(num)

        return 0

    # def image_list(self) -> List[Path]:
    #     """
    #     获取文件夹内的所有图片文件
    #     并且以文件stem的数字排序
    #     :return:
    #     """
    #     file_list = []
    #     for in_file in [Path(pic) for pic in self.pic_list]:
    #         if in_file.is_file() and in_file.suffix.lower() in IMAGE_FILE_SUFFIX:
    #             file_list.append(in_file)
    #
    #     file_list.sort(key=lambda k: self.get_stem(k))
    #
    #     return file_list

    def pil_list(self) -> List[Image.Image]:
        """
        根据排序后的图片列表
        构建 PIL 列表
        :return:
        """
        pil_list = []
        for in_file in self.pic_list:
            pil_list.append(
                Image.open(in_file)
            )

        return pil_list

    def x_merge(self) -> Image.Image:
        """
        横向粘贴所有图片
        :return:
        """
        pil_list = self.pil_list()

        bg_width = 0
        average_height = int(sum([pil.height for pil in pil_list]) / len(pil_list))

        for pil in pil_list:
            bg_width += int(pil.width / (pil.height / average_height)) + self.gutter

        bg = Image.new('RGBA', (bg_width, average_height), (255, 255, 255))

        left = 0
        for pil in pil_list:
            bg_width = int(pil.width / (pil.height / average_height))
            pil = pil.resize((bg_width, average_height), resample=Image.Resampling.LANCZOS)
            bg.paste(
                pil, (left, 0)
            )
            left += pil.width + self.gutter
            pil.close()

        return bg

    def y_merge(self) -> Image.Image:
        """
        竖向粘贴所有图片
        :return:
        """
        pil_list = self.pil_list()

        bg_height = 0
        average_width = int(
            sum([pil.width for pil in pil_list]) / len(pil_list)
        )

        for pil in pil_list:
            bg_height += int(
                pil.height / (pil.width / average_width)
            ) + self.gutter

        bg = Image.new('RGBA', (average_width, bg_height), (255, 255, 255))
        top = 0

        for pil in pil_list:
            bg_height = int(
                pil.height / (pil.width / average_width)
            )
            pil = pil.resize((average_width, bg_height), resample=Image.Resampling.LANCZOS)
            bg.paste(
                pil, (0, top)
            )
            top += pil.height + self.gutter
            pil.close()

        return bg

    def one_two_merge(self):
        first_pil = self.pil_list()[0]


    def main(self):
        bg: Optional[Image.Image] = None

        if self.direction == 'x':
            bg = self.x_merge()

        elif self.direction == 'y':
            bg = self.y_merge()

        elif self.direction == '1-2':
            pass

        bg.save(
            self.folder.parent / (self.folder.stem + ".png")
        )


if __name__ == '__main__':
    ami = AutoMergeImage.open_path(r"V:\H000-H999\H0633\H0633", pic_list=[
        r"V:\H000-H999\H0633\H0633\画板 2.png", r"V:\H000-H999\H0633\H0633\1 (14).png"
    ])
    ami.direction = 'y'
    pic = ami.main()
    pic.save(
        r"V:\H000-H999\H0633\H0633\1-14.png"
    )
