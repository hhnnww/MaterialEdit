import re
from pathlib import Path
from typing import Optional, List
from uuid import uuid1

from PIL import Image
from fastapi import APIRouter
from pydantic import BaseModel

from module_素材处理.core.setting import IMAGE_FILE_SUFFIX

router = APIRouter(prefix='/图片自动拼图', tags=['自动拼图'])


class ItemGetPic(BaseModel):
    in_folder: str


@router.post('/获取所有图片')
def get_pic_list(item_in: ItemGetPic):
    pic_path_list = []
    for in_file in Path(item_in.in_folder).iterdir():
        if in_file.is_file() and in_file.suffix.lower() in IMAGE_FILE_SUFFIX:
            pic_path_list.append(
                dict(
                    path=in_file.as_posix(),
                    name=in_file.name
                )
            )
    return dict(pic_list=pic_path_list)


class ItemMakePic(BaseModel):
    in_folder: str
    pic_list: List[str]
    direction: str
    gutter: int


@router.post('/制作合并图')
def make_merge_pic(item_in: ItemMakePic):
    mk_pic = AutoMergeImage.open_path(
        folder=item_in.in_folder,
        pic_list=item_in.pic_list,
        direction=item_in.direction,
    )
    mk_pic.gutter = item_in.gutter
    mk_pic.main()


# --------------- 图片粘贴到一起 ---------------

class AutoMergeImage:
    direction: str = 'y'
    folder: Optional[Path] = None
    gutter: int = 0
    pic_list: Optional[List[str]] = None

    @classmethod
    def open_path(cls, folder: str, pic_list: List[str], direction: str = 'y'):
        """
        传入文件夹
        和图片列表
        :param folder: 文件夹，图片将会保存在文件夹上层
        :param pic_list: 图片列表
        :param direction: 排列方式
        :return:
        """
        cls.folder = Path(folder)
        cls.pic_list = pic_list
        cls.direction = direction
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

    def image_list(self) -> List[Path]:
        """
        获取文件夹内的所有图片文件
        并且以文件stem的数字排序
        :return:
        """
        file_list = []
        for in_file in [Path(pic) for pic in self.pic_list]:
            if in_file.is_file() and in_file.suffix.lower() in IMAGE_FILE_SUFFIX:
                file_list.append(in_file)

        file_list.sort(key=lambda k: self.get_stem(k))
        return file_list

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

    def x_merge(self, pil_list: List[Image.Image]) -> Image.Image:
        """
        横向粘贴所有图片
        :return:
        """
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

    def y_merge(self, pil_list: List[Image.Image]) -> Image.Image:
        """
        竖向粘贴所有图片
        :return:
        """
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

    def one_two_merge(self, pil_list: List[Image.Image]):
        new_list = []
        in_list = []

        for num, pil in enumerate(pil_list):
            in_list.append(pil)

            if num == 0:
                new_list.append(in_list)
                in_list = []

            elif num > 0 and len(in_list) == 2:
                new_list.append(in_list)
                in_list = []

            elif num == len(pil_list) - 1 and len(in_list) > 0:
                new_list.append(in_list)
                in_list = []

        new_pil_list = []
        for in_list in new_list:
            new_pil_list.append(self.x_merge(in_list))

        return self.y_merge(new_pil_list)

    def main(self):
        bg: Optional[Image.Image] = None

        if self.direction == 'x':
            bg = self.x_merge(self.pil_list())

        elif self.direction == 'y':
            bg = self.y_merge(self.pil_list())

        elif self.direction == '1-2':
            bg = self.one_two_merge(self.pil_list())

        bg.save(
            self.folder / (uuid1().hex.upper() + ".png")
        )


if __name__ == '__main__':
    ami = AutoMergeImage.open_path(
        folder=r"H:\泡泡素材\0000-0999\0001\效果图\avira-powerpoint-template",
        pic_list=[
            r"H:\泡泡素材\0000-0999\0001\效果图\avira-powerpoint-template\1.png",
            r"H:\泡泡素材\0000-0999\0001\效果图\avira-powerpoint-template\2.png",
            r"H:\泡泡素材\0000-0999\0001\效果图\avira-powerpoint-template\3.png",
            r"H:\泡泡素材\0000-0999\0001\效果图\avira-powerpoint-template\4.png",
        ]
    )
    ami.direction = '1-2'
    ami.main()
