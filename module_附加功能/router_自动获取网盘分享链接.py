from pathlib import Path
from typing import Union

import pyautogui
import pyperclip
from fastapi import APIRouter
from pydantic import BaseModel

pyautogui.PAUSE = 1

router = APIRouter(prefix='/自动分享网盘链接', tags=['自动分享网盘链接'])


class ItemIn(BaseModel):
    start_num: str
    end_num: str


@router.post('/')
def fun_自动分享网盘链接(item_in: ItemIn):
    AutoGetBaiDuYunShareLink(
        start_num=int(item_in.start_num),
        end_num=int(item_in.end_num)
    ).run()


class AutoGetBaiDuYunShareLink:
    def __init__(self, start_num: int, end_num: int):
        self.start_num = start_num
        self.end_num = end_num

    @staticmethod
    def fun_根据图片获取需要点击的位置(img: str) -> Union[tuple, None]:
        """
        传入图片，获取图片中心位置
        :param img:
        :return:
        """
        img = Path(__file__).parent.parent / img
        position = pyautogui.locateOnScreen(img.as_posix())

        if position is None:
            return None

        cl = position.left + int(position.width / 2)
        ct = position.top + int(position.height / 2)
        return cl, ct

    @staticmethod
    def fun_处理网盘分享内容(bd_share_content: str) -> str:
        """
        删除网盘分享链接的广告语
        :param bd_share_content:
        :return:
        """
        bd_share_content = bd_share_content.split('\n')[:-1]
        bd_share_content = '\n'.join(bd_share_content)
        bd_share_content = bd_share_content.rstrip()

        return bd_share_content

    def fun_获取百度网盘地址(self, ma_id: str) -> str:
        """
        自动从百度网盘获取分享链接
        :param ma_id:
        :return:
        """
        # 点击搜搜框
        pyautogui.click(3629, 122)

        # 全选并删除
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('del')

        # 输入文字
        pyautogui.write(ma_id)
        pyautogui.hotkey('enter')
        pyautogui.sleep(1)

        # 找到文件夹
        res = self.fun_根据图片获取需要点击的位置('IMG/bd-folder.png')
        if res is None:
            return

        cl, ct = res
        pyautogui.rightClick(cl, ct)

        # 分享按钮
        cl, ct = self.fun_根据图片获取需要点击的位置('IMG/bd-share.png')
        pyautogui.click(cl, ct)

        # 永久有效
        cl, ct = self.fun_根据图片获取需要点击的位置('IMG/bd-time.png')
        pyautogui.click(cl, ct)

        # 创建连接
        cl, ct = self.fun_根据图片获取需要点击的位置('IMG/bd-getlink.png')
        pyautogui.click(cl, ct)

        # 关闭
        while self.fun_根据图片获取需要点击的位置('IMG/bd-close.png') is None:
            pyautogui.sleep(1)

        cl, ct = self.fun_根据图片获取需要点击的位置('IMG/bd-close.png')
        pyautogui.click(cl, ct)

        bd_share = self.fun_处理网盘分享内容(pyperclip.paste())

        print(
            f'{ma_id}\t"{bd_share}"\n'
        )

        return f'{ma_id}\t"{bd_share}"\n\n'

    def run(self):
        output = Path().home() / 'Desktop' / 'output.txt'

        f = open(output.as_posix(), 'w+')
        f.close()

        # 打开百度网盘在任务栏的位置
        c_l, c_t = self.fun_根据图片获取需要点击的位置('IMG/bd-icon.png')
        pyautogui.click(c_l, c_t)

        with open(output.as_posix(), 'a+') as f:
            for x in range(self.start_num, self.end_num + 1):
                f.write(self.fun_获取百度网盘地址(str(x)))

        pyautogui.alert('自动获取百度网盘链接已经处理完成！')


if __name__ == '__main__':
    AutoGetBaiDuYunShareLink(
        start_num=2291,
        end_num=2291
    ).run()
