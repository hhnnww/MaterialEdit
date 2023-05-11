import os
import re
from pathlib import Path

import pyautogui
import pyperclip
from fastapi import APIRouter
from pydantic import BaseModel

from module_附加功能.fun_根据图片查找点击位置 import fun_根据图片获取需要点击的位置

pyautogui.PAUSE = .5

router = APIRouter(prefix='/自动上传到百度网盘', tags=['自动上传到百度网盘'])


class ItemIn(BaseModel):
    start_path: str


@router.post('')
def up_baidu_yun(item_in: ItemIn):
    AutoUpToBaiDuYun(item_in.start_path).run()


class AutoUpToBaiDuYun:
    def __init__(self, start_path: str):
        self.start_path = Path(start_path)

    @staticmethod
    def get_stem(stem: str) -> int:
        """
        根据目录找到 num
        :param stem:
        :return:
        """
        stem_num = re.findall(r'\d+', stem)[0]
        stem_num = int(stem_num)
        return stem_num

    def get_all_path(self, in_path: Path):
        """
        找到所有目录
        :param in_path:
        :return:
        """
        for dst_path in in_path.parent.iterdir():
            if dst_path.is_dir() and self.get_stem(dst_path.stem) >= self.get_stem(self.start_path.stem):
                yield dst_path

    @staticmethod
    def up_path_to_bd(in_path: Path):
        """
        操作单个文件夹上传到百度网盘
        :param in_path:
        :return:
        """
        pyperclip.copy(in_path.as_posix())

        # 地址栏
        while fun_根据图片获取需要点击的位置("IMG/file-address.png") is None:
            pyautogui.sleep(.5)

        cl, ct = fun_根据图片获取需要点击的位置("IMG/file-address.png")
        pyautogui.click(cl, ct)

        pyautogui.hotkey('ctrl', 'v')
        pyautogui.hotkey('enter')

        # 点文件夹
        cl, ct = fun_根据图片获取需要点击的位置("IMG/file-name.png")
        pyautogui.click(cl, ct + 50)

        # shift + f10
        pyautogui.hotkey('shift', 'f10')

        # 点击百度网盘上传
        while fun_根据图片获取需要点击的位置("IMG/file-upbd.png") is None:
            pyautogui.sleep(.5)

        cl, ct = fun_根据图片获取需要点击的位置("IMG/file-upbd.png")
        pyautogui.click(cl, ct)

    def run(self):
        # 开始运行
        # 必须提前打开文件管理器，并且最大化
        os.startfile(r'C:\Users\wuweihua')

        for dp in self.get_all_path(in_path=self.start_path):
            print(dp)
            self.up_path_to_bd(dp)

        pyautogui.alert('自动上传到百度网盘完成。', "素材全自动处理程序")


if __name__ == '__main__':
    AutoUpToBaiDuYun(r'F:\小夕素材\10000-10999\10044').run()
