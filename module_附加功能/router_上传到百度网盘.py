import re
from pathlib import Path

import pyautogui
import pyperclip
from fastapi import APIRouter
from pydantic import BaseModel
from module_附加功能.router_自动获取网盘分享链接 import AutoGetBaiDuYunShareLink

pyautogui.PAUSE = 1

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

        # 点任务栏
        # pyautogui.click(2023, 2130)

        # 地址栏
        pyautogui.click(1000, 162)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.hotkey('enter')

        # 点文件夹
        pyautogui.click(587, 278)

        # shift + f10
        pyautogui.hotkey('shift', 'f10')
        pyautogui.sleep(1)

        # 点击百度网盘上传
        pyautogui.click(582, 985)
        pyautogui.sleep(1)

    def run(self):
        # 开始运行
        # 必须提前打开文件管理器，并且最大化
        cl, ct = AutoGetBaiDuYunShareLink.fun_根据图片获取需要点击的位置('IMG/file-manter.png')
        pyautogui.click(cl, ct)

        for dp in self.get_all_path(in_path=self.start_path):
            print(dp)
            self.up_path_to_bd(dp)

        pyautogui.alert('自动上传到百度网盘完成。', "素材全自动处理程序")
